import struct
import librtmp
import av
import queue
import threading
from concurrent.futures import ThreadPoolExecutor
import ctypes
import socket
from time import time
from loguru import logger
from datetime import timedelta
import numpy as np

class RTMPSender:
    def __init__(self, ip_address, port, frame_size, rtmp_url, my_logger=None, gop=25, hard_encode=False, open_log=False, days=7, stdout=False, log_dir='./logs/', bit_rate=600000):
        self.image_queue2 = queue.Queue()
        self.audio_queue2 = queue.Queue()
        self.image_file = ""
        self.audio_file = ""
        self.ip_address = ip_address
        self.port = port
        self.output_path = 'output.mp4'
        self.hard_encode = hard_encode
        self.open_log = open_log
        self.gop = gop
        self.logger = my_logger
        self.rtmp_url = rtmp_url


        # 默认video img RTMP header参数
        self.RTP_VIDEO_IMG_TIMESTAMP = 0
        # 默认音频bytes RTMP header 参数
        self.RTP_AUDIO_BYTES_TIMESTAMP = 0

        self.max_payload_size = 1400

        self.img_rtp_sent_total_time = 0
        self.img_rtp_sent_total_cnt = 0
        self.img_encode_total_time = 0
        self.img_encode_total_cnt = 0
        self.audio_rtp_sent_total_time = 0
        self.audio_rtp_sent_total_cnt = 0

        # 初始化输出容器
        self.output_container = av.open(self.output_path, mode='w')

        if self.logger is None:
            if not stdout:
                logger.remove() # 移除默认的日志记录器：控制台打印
            logger.add(
                log_dir + "rtp_sender.{time:YYYY-MM-DD_HH}.log", 
                rotation="1 hour",  # 每小时创建一个新日志文件
                retention=timedelta(days=days),  # 保留最近days天的日志，默认为7天
                compression=None,  # 不压缩日志文件
                format="{time:YYYY-MM-DD at HH:mm:ss.SSS} | {level} | {message}"
            )
            self.logger = logger

        # 创建视频流
        if self.hard_encode:
            if self.open_log:
                self.logger.info("use hard_encode...")
            # 视频编码器
            self.video_stream = self.output_container.add_stream('h264_nvenc', rate=25)
            self.video_stream.options = {
                'bf': '0',       # 禁用B帧
                'delay': '0',     # 设置delay为0
                'g': str(self.gop)   # 设置gop大小为25帧
            }
            self.video_stream.pix_fmt = 'yuv420p'
            # self.video_stream.pix_fmt = 'bgr24'

            # 音频编码器
            self.sample_rate = 48000
            self.audio_stream = self.output_container.add_stream('aac', rate=self.sample_rate)
            self.audio_stream.channels = 1
            self.audio_stream.layout = 'mono'  # 声道布局为单声道
            self.audio_stream.format = 'fltp'  # AAC 格式通常使用浮点数据
            # self.audio_stream.bit_rate = 256000
        else:
            if self.open_log:
                self.logger.info("use soft_encode...")
            self.video_stream = self.output_container.add_stream('libx264', rate=25)
            self.video_stream.options = {'g': str(self.gop), 'tune': 'zerolatency'}  # 设置GOP大小为25帧，实现低延迟

        self.video_stream.bit_rate = bit_rate

        if self.open_log:
            self.logger.info(f"bit_rate: {self.video_stream.bit_rate}")
        
        if self.open_log:
            self.logger.info(f"video_stream options: {self.video_stream.options}")

        self.video_stream.width = frame_size[0]
        self.video_stream.height = frame_size[1]

        self.video_frame_cnt = 0
        self.audio_frame_cnt = 0

        self.rtmp_stream = self.create_stream()
        self.write_flv_header()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 655360)  # 设置为64KB

        self.stop_event = threading.Event()

        self.video_thread2 = threading.Thread(target=self.process_video_queue2)
        self.audio_thread2 = threading.Thread(target=self.process_audio_queue2)

        self.video_thread2.start()
        self.audio_thread2.start()

    def stop(self):
        def stop_threads():
            self.stop_event.set()
            self.video_thread2.join()
            self.audio_thread2.join()
            if self.open_log:
                self.logger.info("Threads stopped")

            self.output_container.close()
            if self.open_log:
                self.logger.info("Output container closed")

        if self.open_log:
            self.logger.info("Stopping threads")

        executor = ThreadPoolExecutor(max_workers=1)
        executor.submit(stop_threads)
        executor.shutdown(wait=False)

    def create_stream(self):
        connection = librtmp.RTMP(self.rtmp_url, live=True)

        self.logger.info("connecting to RTMP server...")
        if not connection.connect():
            self.logger.info("connection failed.")
            exit(1)
        else:
            self.logger.info("connection success.")

        self.logger.info("creating stream...")
        stream = connection.create_stream(writeable=True)
        if not stream:
            self.logger.info("creating stream failed.")
            exit(1)
        else:
            self.logger.info("creating stream success.")
        
        return stream
    
    def write_flv_header(self):
        flv_header = b'FLV\x01\x05\x00\x00\x00\x09'  # FLV version 1, contains both audio and video
        self.rtmp_stream.write(flv_header)

    def write_previous_tag_size(self, flv_tag):
        # 上一个标签的大小（包含头和数据）
        prev_tag_size = struct.pack('>I', len(flv_tag))
        self.rtmp_stream.write(prev_tag_size)
    
    def create_flv_video_tag(self, video_data, is_keyframe=False):
        tag_type = 0x09  # 0x09 for video
        data_size = len(video_data) + 5
        stream_id = 0  # Always 0 for StreamID
        
        # Frame Type (4 bits) + CodecID (4 bits)
        frame_type = 1 if is_keyframe else 2  # 1 for keyframe, 2 for interframe
        codec_id = 7  # 7 for AVC (H.264)
        video_frame_header = struct.pack('>B', (frame_type << 4) | codec_id)  # First byte

        # AVC Packet Type (1 byte), 0 = AVC sequence header, 1 = NALU
        avc_packet_type = 1  # 1 for NALU (actual video frame)
        
        # Composition Time (3 bytes)
        composition_time = struct.pack('>I', 0)[1:]

        # FLV Tag Header (11 bytes)
        tag_header = struct.pack(
            '>B3s3sB3s',
            tag_type,  # 1 byte - Tag Type (0x09 for video)
            struct.pack('>I', data_size)[1:],  # 3 bytes - Data Size
            struct.pack('>I', self.RTP_VIDEO_IMG_TIMESTAMP)[1:],  # 3 bytes - Timestamp
            (self.RTP_VIDEO_IMG_TIMESTAMP >> 24) & 0xFF,  # 1 byte - Timestamp Extended
            struct.pack('>I', stream_id)[1:],  # 3 bytes - StreamID
        )

        flv_tag = tag_header + video_frame_header + struct.pack('>B', avc_packet_type) + composition_time + video_data

        return flv_tag
    
    def create_flv_audio_tag(self, audio_data, is_sequence_header=False):
        # 设定参数
        audio_format = 10  # AAC
        sound_rate = 3  # 44.1kHz
        sound_size = 1  # 16-bit
        sound_type = 0  # Mono
        stream_id = 0

        data_length = len(audio_data)

        # Tag Header
        tag_type = 8  # Audio
        tag_data_size = data_length + 2  # 加上参数字节
        
        tag_header = struct.pack(
            '>B3s3sB3s',
            tag_type,  # 1 byte - Tag Type (0x09 for video)
            struct.pack('>I', tag_data_size)[1:],  # 3 bytes - Data Size
            struct.pack('>I', self.RTP_AUDIO_BYTES_TIMESTAMP)[1:],  # 3 bytes - Timestamp
            (self.RTP_AUDIO_BYTES_TIMESTAMP >> 24) & 0xFF,  # 1 byte - Timestamp Extended
            struct.pack('>I', stream_id)[1:],  # 3 bytes - StreamID
        )

        # 构建音频数据，第一个字节是音频数据的参数
        audio_header = (audio_format << 4) | (sound_rate << 2) | (sound_size << 1) | sound_type
        aac_packet_type = 0 if is_sequence_header else 1
        audio_data_with_header = bytes([audio_header, aac_packet_type]) + audio_data

        return tag_header + audio_data_with_header
    
    def get_aac_sequence_header_data(self, sample_rate, channels, profile=2):
        """
        Generate AAC sequence header (AudioSpecificConfig) for FLV.
        
        :param sample_rate: The sample rate of the AAC stream (e.g., 44100).
        :param channels: The number of audio channels (e.g., 1 for mono, 2 for stereo).
        :param profile: AAC profile (default is 2 for AAC-LC).
        :return: AAC sequence header as bytes.
        """
        # Sample rate index based on the table
        sample_rate_index = {
            96000: 0, 88200: 1, 64000: 2, 48000: 3,
            44100: 4, 32000: 5, 24000: 6, 22050: 7,
            16000: 8, 12000: 9, 11025: 10, 8000: 11
        }[sample_rate]

        # Create the AudioSpecificConfig (2 bytes)
        audio_specific_config = (profile << 11) | (sample_rate_index << 7) | (channels << 3)
        
        # Convert to bytes (16-bit big-endian)
        return audio_specific_config.to_bytes(2, 'big')
    
    def generate_adts_header(self, sample_rate, channels, aac_frame_length):
        # ADTS头由7个字节组成
        adts_header = bytearray(7)

        # AAC 固定参数
        profile = 1  # AAC LC
        freq_idx = {
            96000: 0, 88200: 1, 64000: 2, 48000: 3, 44100: 4,
            32000: 5, 24000: 6, 22050: 7, 16000: 8, 12000: 9,
            11025: 10, 8000: 11, 7350: 12
        }[sample_rate]
        chan_cfg = channels

        # 设置ADTS头部
        # adts_header[0] = 0xFF
        # adts_header[1] = 0xF1  # 0xF1 如果没有 CRC校验, 否则 0xF9
        # adts_header[2] = ((profile << 6) + (freq_idx << 2) + (chan_cfg >> 2))
        # adts_header[3] = (((chan_cfg & 3) << 6) + (aac_frame_length >> 11))
        # adts_header[4] = ((aac_frame_length & 0x7FF) >> 3)
        # adts_header[5] = (((aac_frame_length & 7) << 5) + 0x1F)
        # adts_header[6] = 0xFC

        adts_header[0] = ((profile << 6) + (freq_idx << 2) + (chan_cfg >> 2))
        adts_header[1] = (((chan_cfg & 3) << 6) + (aac_frame_length >> 11))
        adts_header[2] = ((aac_frame_length & 0x7FF) >> 3)
        adts_header[3] = (((aac_frame_length & 7) << 5) + 0x1F)
        adts_header[4] = 0xFC

        return adts_header

    def send_video_rtmp_from_img(self, img):
        img_frame = av.VideoFrame.from_ndarray(img, format = 'rgb24')
        self.image_queue2.put(img_frame)

    def process_video_queue2(self):
        if self.open_log:
            self.logger.info("Processing video queue from img")

        sent_cnt = 0

        while not self.stop_event.is_set():
            try:
                img_frame = self.image_queue2.get(block=True, timeout=5)
                if self.open_log:
                    self.logger.info(f"len(image_queue2): {self.image_queue2.qsize()}")
            except queue.Empty:
                continue

            encode_begin = time()
            packets = self.video_stream.encode(img_frame)
            encode_end = time()
            cur_encode_cost_time = (encode_end - encode_begin) * 1000
            self.img_encode_total_time += cur_encode_cost_time
            self.img_encode_total_cnt += 1
            if self.open_log:
                self.logger.info(f"No. {self.img_encode_total_cnt} img encode time: {cur_encode_cost_time}ms")
                self.logger.info(f"img encode avg time: {self.img_encode_total_time / self.img_encode_total_cnt}ms")

            send_begin = time()

            data = self.video_stream.codec_context.extradata

            for packet in packets:
                buffer_ptr = packet.buffer_ptr
                buffer_size = packet.buffer_size
                buffer = (ctypes.c_char * buffer_size).from_address(buffer_ptr)

                buffer_bytes = bytes(buffer)

                is_keyframe = False

                begin = b'\x00\x00\x01\x06'
                end = b'\x00\x00\x00\x01\x65'
                p = b'\x00\x00\x00\x01\x61'
                
                if self.hard_encode:
                    if buffer_bytes.find(begin) != -1:
                        is_keyframe = True
                        pos = buffer_bytes.find(end)
                        if pos != -1:
                            buffer = data + buffer[pos:]
                        else:
                            pos2 = buffer_bytes.find(p)
                            if pos2 != -1:
                                buffer = buffer[pos2:]
                    elif buffer_bytes.startswith(end):
                        buffer = data + buffer
                else:
                    if buffer_bytes.startswith(begin):
                        pos = buffer_bytes.find(end)
                        if pos != -1:
                            buffer = data + buffer[pos:]
                    elif buffer_bytes.startswith(end):
                        buffer = data + buffer

                payload = buffer

                flv_video_tag = self.create_flv_video_tag(payload, is_keyframe)
                self.rtmp_stream.write(flv_video_tag)
                self.logger.info("flv_video_tag send done!")

                sent_cnt += 1
                
                self.RTP_VIDEO_IMG_TIMESTAMP += 40
                
                self.video_frame_cnt += 1
            send_end = time()
            cur_img_send_cost_time = (send_end - send_begin) * 1000
            self.img_rtp_sent_total_time += cur_img_send_cost_time
            self.img_rtp_sent_total_cnt += 1
            if self.open_log:
                self.logger.info(f"No. {self.img_rtp_sent_total_cnt} img rtmp send time: {cur_img_send_cost_time}ms")
                self.logger.info(f"img rtmp send avg time: {self.img_rtp_sent_total_time / self.img_rtp_sent_total_cnt}ms")

    def send_audio_rtmp_from_bytes(self, audio_bytes, is_16k=False):
        self.audio_queue2.put((audio_bytes, is_16k))


    def process_audio_queue2(self):
        if self.open_log:
            self.logger.info("Processing audio queue from bytes")

        sent_cnt = 0

        sequence_header_sent = False

        while not self.stop_event.is_set():
            try:
                audio_data, _ = self.audio_queue2.get(block=True, timeout=5)
                if self.open_log:
                    self.logger.info(f"len(audio_queue2): {self.audio_queue2.qsize()}")
            except queue.Empty:
                continue

            data = self.audio_stream.codec_context.extradata
            data_size = self.audio_stream.codec_context.extradata_size
            pcm_array = np.frombuffer(audio_data, dtype=np.int16).reshape(1, -1)
            
            audio_frame = av.AudioFrame.from_ndarray(pcm_array, format="s16", layout='mono')
            audio_frame.sample_rate = self.sample_rate

            if not self.audio_stream.codec_context.is_open:
                self.audio_stream.codec_context.open()

            packets = self.audio_stream.encode(audio_frame)


            # adts_header = self.generate_adts_header(self.sample_rate, 1, 18)

            audio_send_begin = time()

            for packet in packets:
                buffer_ptr = packet.buffer_ptr
                buffer_size = packet.buffer_size
                buffer = (ctypes.c_char * buffer_size).from_address(buffer_ptr)
                # print(buffer[0])

                # byte_value = buffer[0]

                if data_size == 0:
                    continue

                # print(int.from_bytes(byte_value, byteorder='big'))

                if not sequence_header_sent:
                    # data = b'\x12\x08V\xe5\x00'
                    # data = b'\x11\x90\x56\xe5\x00'
                    # profile = 1
                    # freq_idx = 4
                    # chan_cfg = 1
                    # aac_frame_length = 18
                    # a = ((profile << 6) + (freq_idx << 2) + (chan_cfg >> 2))
                    # b = (((chan_cfg & 3) << 6) + (aac_frame_length >> 11))
                    flv_audio_tag = self.create_flv_audio_tag(data, is_sequence_header=True)
                    self.rtmp_stream.write(flv_audio_tag)
                    self.logger.info("AAC Sequence Header sent!")
                    sequence_header_sent = True

                payload = buffer

                flv_audio_tag = self.create_flv_audio_tag(payload, is_sequence_header=False)
                self.rtmp_stream.write(flv_audio_tag)
                self.logger.info("flv_audio_tag send done!")

                sent_cnt += 1
                
                self.RTP_AUDIO_BYTES_TIMESTAMP += 20

                self.audio_frame_cnt += 1

            audio_send_end = time()
            cur_audio_send_cost_time = (audio_send_end - audio_send_begin) * 1000
            self.audio_rtp_sent_total_time += cur_audio_send_cost_time
            self.audio_rtp_sent_total_cnt += 1
            if self.open_log:
                self.logger.info(f"No. {self.audio_rtp_sent_total_cnt} audio rtmp send time: {cur_audio_send_cost_time}ms")
                self.logger.info(f"audio rtmp send avg time: {self.audio_rtp_sent_total_time / self.audio_rtp_sent_total_cnt}ms")