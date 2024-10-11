#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2024/09/03 16:45:23
@Author  :   ChenHao
@Description  :   命令行工具
@Contact :   jerrychen1990@gmail.com
'''


from json import load
import os

from loguru import logger
from liteai.api import chat


def batch(data_path: str, model: str, work_num=4, input_column="input", image_column: str = None, image_dir=None):
    """
    批量处理数据
    """
    data = load(data_path)
    logger.info(f"loaded {len(data)} records from {data_path}")
    if image_column:
        assert image_dir, "image_dir is required when image_column is set"
    if not os.path.exists(image_dir):
        raise ValueError(f"image_dir {image_dir} not exists")

    def _func(item):
        message = item[input_column]
        resp = chat(model=model, messages=message, stream=False)
        

