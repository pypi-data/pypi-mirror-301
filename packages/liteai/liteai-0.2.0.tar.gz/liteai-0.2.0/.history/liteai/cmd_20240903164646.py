#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2024/09/03 16:45:23
@Author  :   ChenHao
@Description  :   命令行工具
@Contact :   jerrychen1990@gmail.com
'''


from json import load


def batch(data_path: str, model: str, work_num=4, input_column="input", image_column="image"):
    """
    批量处理数据
    """
    data = load(data_path)
    logger.indo(f"start batch process data: {data_path}")
