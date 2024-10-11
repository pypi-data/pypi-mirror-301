import unittest

import litellm


from liteai.core import Message
from liteai.api import chat
from liteai.utils import set_logger, show_response
from loguru import logger


class TestLiteLLM(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        set_logger(__name__)
        logger.info("start lite llm job")

    def test_sync(self):
        system = "用英文回答我的问题, 80个单词以内"
        question = "列出国土面积最大的五个国家"
        model = "tgi_glm3_32b"
        base_url = "http://hz-model.bigmodel.cn/servyou-api/generate"
        litellm.set_verbose = True
        messages = [Message(role="system", content=system),
                    Message(role="user", content=question)]
        response = chat(model=model, messages=messages, stream=False, base_url=base_url, temperature=0.)
        show_response(response)
