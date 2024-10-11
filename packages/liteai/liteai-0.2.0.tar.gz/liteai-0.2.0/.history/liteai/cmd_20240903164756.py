#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2024/09/03 16:45:23
@Author  :   ChenHao
@Description  :   命令行工具
@Contact :   jerrychen1990@gmail.com
'''


from json import load

from loguru import logger


def batch(data_path: str, model: str, work_num=4, input_column="input", image_column:str, image_dir=""):
    """
    批量处理数据
    """
    data = load(data_path)
    logger.info(f"loaded {len(data)} records from {data_path}")
    def _func(item):
        message = item[input_column]

