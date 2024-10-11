#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2024/07/22 17:29:31
@Author  :   ChenHao
@Description  :   
@Contact :   jerrychen1990@gmail.com
'''


import streamlit as st
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase
import av
from pydub import AudioSegment
import numpy as np

# 生成器函数，模拟音频流


def byte_generator():
    for i in range(10):
        yield (np.random.rand(44100) * 2 - 1).astype(np.float32).tobytes()

# 自定义音频处理器


class AudioProcessor(AudioProcessorBase):
    def __init__(self):
        self.generator = byte_generator()
        self.audio_data = b''

    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        try:
            self.audio_data = next(self.generator)
        except StopIteration:
            pass

        samples = np.frombuffer(self.audio_data, dtype=np.float32)
        new_frame = av.AudioFrame.from_ndarray(samples, layout="mono")
        new_frame.sample_rate = frame.sample_rate
        return new_frame


# 使用 webrtc_streamer 进行实时音频流播放
webrtc_streamer(key="example", audio_processor_factory=AudioProcessor)
