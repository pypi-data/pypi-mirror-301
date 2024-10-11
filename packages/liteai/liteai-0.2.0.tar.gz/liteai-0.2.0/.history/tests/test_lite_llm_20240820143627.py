import unittest


from liteai.core import Message
from liteai.api import chat
from liteai.utils import set_logger, show_response
from loguru import logger

provider = LiteLLMProvider(base_url="http://36.103.167.117:8101")
messages = [Message(role="user", content="你好")]
resp = provider.complete(messages=messages, model="tgi_glm2_12b", stream=False)
print(resp.content)


class TestLiteLLM(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        set_logger(__name__)
        logger.info("start lite llm job")

    def test_sync(self):
        system = "用英文回答我的问题, 80个单词以内"
        question = "列出国土面积最大的五个国家"
        model = "tgi_glm3_32b"
        base_url = "hz-model.bigmodel.cn/"
        messages = [Message(role="system", content=system),
                    Message(role="user", content=question)]
        response = chat(model=model, messages=messages, stream=False, temperature=0.)
        show_response(response)
        # self.assertIsNotNone(response.usage)
        # messages.extend([Message(role="assistant", content=response.content),
        #                 Message(role="user", content="介绍第二个")])
        # response = chat(model=model, messages=messages, stream=False, temperature=0.)
        # show_response(response)
        # self.assertIsNotNone(response.usage)
        # self.assertTrue("Canada" in response.content)

        # response = chat(model=model, messages="你好呀", stream=False, temperature=0., log_level="INFO")
        # show_response(response)
