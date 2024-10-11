#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2024/08/29 14:20:40
@Author  :   ChenHao
@Description  :   讯飞适配器
@Contact :   jerrychen1990@gmail.com
'''
import itertools
from typing import Any, List, Tuple

from loguru import logger
import numpy as np


from liteai.core import ModelCard, ModelResponse, Message, ToolDesc, Usage
from zhipuai import ZhipuAI
from liteai.provider.base import BaseProvider
from snippets import add_callback2gen

from liteai.utils import extract_tool_calls, get_text_chunk, image2base64, acc_chunks


class XunfeiProvider(BaseProvider):
    key: str = "xunfei"
    allow_kwargs = {"stream", "temperature", "top_p", "max_tokens", "meta"}
    api_key_env = "XUNFEI_API_KEY"

    def __init__(self, api_key: str = None, **kwargs):
        super().__init__(api_key=api_key)
        self.client = ZhipuAI(api_key=self.api_key)

    def asr(self, voice: Voice, model: ModelCard, **kwargs) -> Voice:
        raise Exception(f"provider {self.__class__.__name__} not support asr!")
