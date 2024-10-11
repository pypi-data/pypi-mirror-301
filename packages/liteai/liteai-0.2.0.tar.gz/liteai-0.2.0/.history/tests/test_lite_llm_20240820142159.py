import unittest


from liteai.core import Message
from liteai.api import chat, embedding
from liteai.tool import CURRENT_CONTEXT_TOOL
from liteai.utils import get_embd_similarity, set_logger, show_embeds, show_response
from loguru import logger


class TestLiteLLM(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        set_logger(__name__)
        logger.info("start test job")

    def test_sync(self):
        system = "用英文回答我的问题, 80个单词以内"
        question = "列出国土面积最大的五个国家"
        model = "glm-4-air"
        messages = [Message(role="system", content=system),
                    Message(role="user", content=question)]
        response = chat(model=model, messages=messages, stream=False, temperature=0.)
        show_response(response)
        self.assertIsNotNone(response.usage)
        messages.extend([Message(role="assistant", content=response.content),
                        Message(role="user", content="介绍第二个")])
        response = chat(model=model, messages=messages, stream=False, temperature=0.)
        show_response(response)
        self.assertIsNotNone(response.usage)
        self.assertTrue("Canada" in response.content)

        response = chat(model=model, messages="你好呀", stream=False, temperature=0., log_level="INFO")
        show_response(response)