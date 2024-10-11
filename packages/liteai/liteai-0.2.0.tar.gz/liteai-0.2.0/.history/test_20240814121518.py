import threading
import time
from typing import Iterable
from loguru import logger
from pydub import AudioSegment
from pydub.playback import play

import io
chunk_size = 4096 * 10


def gen():
    with open("tests/hello.mp3", "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                return
            logger.debug(f"yielding chunk, with size {len(chunk)}")
            yield chunk
            time.sleep(2)


# byte_stream = list(gen())
byte_stream = gen()


# buffer_size = 4096*10
# audio_buffer = io.BytesIO()

# segments = [AudioSegment.from_file(io.BytesIO(chunk), format="mp3") for chunk in byte_stream]
# for seg in segments:
#     logger.debug(f"segment size: {len(seg.raw_data)}")
#     # play_obj = sa.play_buffer(seg.raw_data,
#     #                           num_channels=seg.channels,
#     #                           bytes_per_sample=seg.sample_width,
#     #                           sample_rate=seg.frame_rate)
#     play(seg)
#     # play_obj.wait_done()


def play_bytes(byte_stream: Iterable[bytes], min_buffer_size=8192*10):
    audio_buffer = io.BytesIO()
    producer_finished = threading.Event()
    offset = 0

    def _buf_reader():
        for chunk in byte_stream:
            logger.debug(f"write {len(chunk)} bytes to buffer")
            audio_buffer.write(chunk)
            audio_buffer.flush()
        producer_finished.set()

    thread = threading.Thread(target=_buf_reader)
    thread.start()

    def play_segment(check_min_size: bool):
        end_offset = audio_buffer.tell()
        raw_size = end_offset - offset
        logger.debug(f"{producer_finished.is_set()=}, {raw_size=}, {offset=}, {end_offset=}")
        if raw_size > 0:
            if not check_min_size or raw_size >= min_buffer_size:
                audio_buffer.seek(offset)
                audio_segment = AudioSegment.from_file(audio_buffer, format="mp3")
                duration = len(audio_segment)
                logger.debug(f"play audio segment with size:{len(audio_segment.raw_data)}, {raw_size=}, duration:{duration}")
                play(audio_segment)
        return end_offset

    while True:
        if producer_finished.is_set():
            offset = play_segment(False)
        else:
            offset = play_segment(True)

        if raw_size <= min_buffer_size:
            time.sleep(0.1)
            continue

        play_segment()

    thread.join()


play_bytes(byte_stream)

# def play_voice(voice: Voice, buffer_size=DEFAULT_VOICE_CHUNK_SIZE):

#     logger.debug(f"{type(voice.byte_stream)=}, {voice.file_path=}")

#     if voice.file_path and os.path.exists(voice.file_path):
#         play_file(voice.file_path)
#     else:
#         logger.debug(f"playing voice from byte stream")
#         import simpleaudio as sa
#         audio_buffer = io.BytesIO()
#         for chunk in voice.byte_stream:
#             # 将每个块写入缓冲区
#             logger.debug(f"write {len(chunk)} bytes, sample:{chunk[:4]} to buffer")
#             audio_buffer.write(chunk)

#             # 检查缓冲区大小，如果达到一定大小，则进行播放
#             if audio_buffer.tell() > buffer_size:  # 例如，每4KB播放一次
#                 # 将缓冲区内容转换为 AudioSegment
#                 audio_buffer.seek(0)
#                 audio_segment = AudioSegment.from_file(audio_buffer, format="mp3")

#                 # 播放音频段
#                 play_obj = sa.play_buffer(audio_segment.raw_data,
#                                           num_channels=audio_segment.channels,
#                                           bytes_per_sample=audio_segment.sample_width,
#                                           sample_rate=audio_segment.frame_rate)
#                 play_obj.wait_done()

#                 # 清空缓冲区
#                 audio_buffer = io.BytesIO()

#         # 播放剩余部分
#         if audio_buffer.tell() > 0:
#             audio_buffer.seek(0)
#             audio_segment = AudioSegment.from_file(audio_buffer, format="mp3")
#             play_obj = sa.play_buffer(audio_segment.raw_data,
#                                       num_channels=audio_segment.channels,
#                                       bytes_per_sample=audio_segment.sample_width,
#                                       sample_rate=audio_segment.frame_rate)
#             play_obj.wait_done()


# with open("tests/dnll.mp3", "rb") as f:
#     mp3_bytes = f.read()


# mp3_file = io.BytesIO(mp3_bytes)

# # Load the MP3 data into an AudioSegment
# audio_segment = AudioSegment.from_file(mp3_file, format="mp3")

# # Define the slice duration (in milliseconds)
# slice_duration = 1000  # 1 second

# # Slice and play audio in a loop with threading


# def play_slice(start, end):
#     slice_segment = audio_segment[start:end]
#     play(slice_segment)


# start_time = 0
# while start_time < len(audio_segment):
#     end_time = start_time + slice_duration
#     # slice_segment = audio_segment[start_time:end_time]
#     # play(slice_segment)

#     thread = threading.Thread(target=play_slice, args=(start_time, end_time))
#     thread.start()
#     import time
#     time.sleep(slice_duration / 1000*0.9)
#     # thread.join()  # Wait for the slice to finish before starting the next one
#     start_time = end_time

# for chunk in byte_stream:
#     # 将每个块写入缓冲区
#     logger.debug(f"get {len(chunk)} bytes, sample:{chunk[:4]} to buffer")

#     audio_buffer.write(chunk)
#     logger.debug(f"buffer size: {audio_buffer.tell()}")

#     # 检查缓冲区大小，如果达到一定大小，则进行播放
#     if audio_buffer.tell() >= buffer_size:  # 例如，每4KB播放一次
#         # 将缓冲区内容转换为 AudioSegment
#         st = time.time()
#         audio_buffer.seek(0)
#         audio_segment = AudioSegment.from_file(audio_buffer, format="mp3")
#         logger.info(f"playing audio segment, with origin size:{audio_buffer.tell()}, size {len(audio_segment.raw_data)}")
#         latency = time.time() - st
#         logger.info(f"convert to audio segment cost {latency} seconds")

#         # 播放音频段
#         play_obj = sa.play_buffer(audio_segment.raw_data,
#                                   num_channels=audio_segment.channels,
#                                   bytes_per_sample=audio_segment.sample_width,
#                                   sample_rate=audio_segment.frame_rate)
#         play_obj.wait_done()

#         # 清空缓冲区
#         audio_buffer = io.BytesIO()

# # 播放剩余部分
# if audio_buffer.tell() > 0:
#     audio_buffer.seek(0)
#     audio_segment = AudioSegment.from_file(audio_buffer, format="mp3")
#     play_obj = sa.play_buffer(audio_segment.raw_data,
#                               num_channels=audio_segment.channels,
#                               bytes_per_sample=audio_segment.sample_width,
#                               sample_rate=audio_segment.frame_rate)
#     play_obj.wait_done()
