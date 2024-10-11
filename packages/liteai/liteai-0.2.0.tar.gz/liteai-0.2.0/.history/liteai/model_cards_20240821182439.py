#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2024/08/21 18:22:06
@Author  :   ChenHao
@Description  :   
@Contact :   jerrychen1990@gmail.com
'''


from liteai.core import ModelCard

ZHIPU_MODELS = ["glm-4-0520", "glm-4v", "glm-4-air", "glm-4-flash"]
OPENAI_MODELS = ["gpt-4o", "gpt-4", "gpt-4o-mini"]
MINIMAX_MODELS = ["abab6.5s-chat", "speech-01-turbo"]
QWEN_MODELS = ["qwen-turbo", "qwen-vl-plus"]


ZHIPU_MODELS = [
    ModelCard(name="glm-4-0520", description="glm-4-0520", provider="zhipu"),
    ModelCard(name="glm-4-air", description="glm-4-0520", provider="zhipu"),
    ModelCard(name="glm-4-flash", description="glm-4-0520", provider="zhipu"),
    ModelCard(name="glm-4v", description="glm-4-0520", provider="zhipu", support_vision=True)
]

OPENAI_MODELS = [
    ModelCard(name="gpt-4o", description="gpt-4o", provider="openai"),
    ModelCard(name="gpt-4", description="gpt-4", provider="openai"),
    ModelCard(name="gpt-4o-mini", description="gpt-4o-mini", provider="openai")
]
