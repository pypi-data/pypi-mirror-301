#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2024/08/29 14:20:40
@Author  :   ChenHao
@Description  :   讯飞适配器
@Contact :   jerrychen1990@gmail.com
'''
import datetime

import websocket


from liteai.core import ModelCard, Voice
from liteai.provider.base import BaseProvider
from wsgiref.handlers import format_date_time
from time import mktime
import websocket
import datetime
import hashlib
import base64
import hmac
from urllib.parse import urlencode
import ssl
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime


def create_url(api_key, api_secret):
    url = 'wss://ws-api.xfyun.cn/v2/iat'
    # 生成RFC1123格式的时间戳
    now = datetime.now()
    date = format_date_time(mktime(now.timetuple()))

    date = format_date_time(mktime(now.timetuple()))

    # 拼接字符串
    signature_origin = "host: " + "ws-api.xfyun.cn" + "\n"
    signature_origin += "date: " + date + "\n"
    signature_origin += "GET " + "/v2/iat " + "HTTP/1.1"
    # 进行hmac-sha256进行加密
    signature_sha = hmac.new(api_secret.encode('utf-8'), signature_origin.encode('utf-8'),
                             digestmod=hashlib.sha256).digest()
    signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')

    authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
        api_key, "hmac-sha256", "host date request-line", signature_sha)
    authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
    # 将请求的鉴权参数组合为字典
    v = {
        "authorization": authorization,
        "date": date,
        "host": "ws-api.xfyun.cn"
    }
    # 拼接鉴权参数，生成url
    url = url + '?' + urlencode(v)
    # print("date: ",date)
    # print("v: ",v)
    # 此处打印出建立连接时候的url,参考本demo的时候可取消上方打印的注释，比对相同参数时生成的url与自己代码生成的url是否一致
    # print('websocket url :', url)
    return url


class XunfeiProvider(BaseProvider):
    key: str = "xunfei"
    allow_kwargs = {"stream", "temperature", "top_p", "max_tokens", "meta"}
    api_key_env = "XUNFEI_API_KEY"

    def __init__(self, api_key: str = None, **kwargs):
        super().__init__(api_key=api_key)

    def asr(self, voice: Voice, model: ModelCard, **kwargs) -> str:
        global whole_dict
        global wsParam
        whole_dict = {}
        # wsParam1 = Ws_Param(APPID=APPID, APISecret=APISecret,
        #                     APIKey=APIKey, BusinessArgs=BusinessArgsASR,
        #                     AudioFile=AudioFile)
        # wsParam是global变量，给上面on_open函数调用使用的
        # wsParam = wsParam1
        websocket.enableTrace(False)
        ws_url = create_url()
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
