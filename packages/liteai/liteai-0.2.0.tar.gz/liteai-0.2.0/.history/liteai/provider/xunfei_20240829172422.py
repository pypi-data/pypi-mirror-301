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


from liteai.core import ModelCard, ModelResponse, Message, ToolDesc, Usage, Voice
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

    def asr(self, voice: Voice, model: ModelCard, **kwargs) -> str:
        global whole_dict
        global wsParam
        whole_dict = {}
        websocket.enableTrace(False)
    wsUrl = wsParam.create_url()
    ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.on_open = on_open
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
    # 把字典的值合并起来做最后识别的输出
    whole_words = ""
    for i in sorted(whole_dict.keys()):
        whole_words += whole_dict[i]
    return whole_words
        wsParam1 = Ws_Param(APPID=APPID, APISecret=APISecret,
                            APIKey=APIKey, BusinessArgs=BusinessArgsASR,
                            AudioFile=AudioFile)
        # wsParam是global变量，给上面on_open函数调用使用的
        wsParam = wsParam1
        websocket.enableTrace(False)
        wsUrl = wsParam.create_url()
        ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close)
        ws.on_open = on_open
        ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
        # 把字典的值合并起来做最后识别的输出
        whole_words = ""
        for i in sorted(whole_dict.keys()):
            whole_words += whole_dict[i]
        return whole_words

        raise Exception(f"provider {self.__class__.__name__} not support asr!")
