import time
from pydub import AudioSegment
from loguru import logger
import simpleaudio as sa
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


byte_stream = list(gen())


buffer_size = 4096*10
audio_buffer = io.BytesIO()


for chunk in byte_stream:
    # 将每个块写入缓冲区
    logger.debug(f"get {len(chunk)} bytes, sample:{chunk[:4]} to buffer")

    audio_buffer.write(chunk)
    logger.debug(f"buffer size: {audio_buffer.tell()}")

    # 检查缓冲区大小，如果达到一定大小，则进行播放
    if audio_buffer.tell() >= buffer_size:  # 例如，每4KB播放一次
        # 将缓冲区内容转换为 AudioSegment
        st = time.time()
        audio_buffer.seek(0)
        audio_segment = AudioSegment.from_file(audio_buffer, format="mp3")
        logger.info(f"playing audio segment, with origin size:{audio_buffer.tell()}, size {len(audio_segment.raw_data)}")

        # 播放音频段
        play_obj = sa.play_buffer(audio_segment.raw_data,
                                  num_channels=audio_segment.channels,
                                  bytes_per_sample=audio_segment.sample_width,
                                  sample_rate=audio_segment.frame_rate)
        play_obj.wait_done()

        # 清空缓冲区
        audio_buffer = io.BytesIO()

# 播放剩余部分
if audio_buffer.tell() > 0:
    audio_buffer.seek(0)
    audio_segment = AudioSegment.from_file(audio_buffer, format="mp3")
    play_obj = sa.play_buffer(audio_segment.raw_data,
                              num_channels=audio_segment.channels,
                              bytes_per_sample=audio_segment.sample_width,
                              sample_rate=audio_segment.frame_rate)
    play_obj.wait_done()
