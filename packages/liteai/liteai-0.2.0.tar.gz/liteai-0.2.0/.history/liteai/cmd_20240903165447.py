#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2024/09/03 16:45:23
@Author  :   ChenHao
@Description  :   命令行工具
@Contact :   jerrychen1990@gmail.com
'''


import os
import time

import click
from loguru import logger
from liteai.api import chat
from snippets.decorators import multi_thread
from sni


@click.command()
@click.option("--model", "-m", help="模型名称")
@click.option("--data_path", "-d", help="输入文件路径，支持.xlsx, .csv, .json")
@click.option("--work_num", "-w", default=4, help="并发数")
@click.option("--input_column", "-i", default="input", help="输入列名")
@click.option("--image_column", help="图片列名")
@click.option("--image_dir", help="图片目录, 输入图片列名时必须存在")
def batch(data_path: str, model: str, work_num=4, input_column="input", image_column: str = None, image_dir=None):
    """
    批量处理数据
    """
    st= time.time()
    data = load(data_path)
    logger.info(f"loaded {len(data)} records from {data_path}")
    if image_column:
        assert image_dir, "image_dir is required when image_column is set"
    if not os.path.exists(image_dir):
        raise ValueError(f"image_dir {image_dir} not exists")

    def _func(item):
        message = item[input_column]
        resp = chat(model=model, messages=message, stream=False)
        item["response"] = resp.content
    batch_func = multi_thread(work_num=work_num, return_list=True)(_func)
    batch_func(data=data)
    logger.info(f"processed {len(data)} records in {time.time()-st:.2f} seconds, dump to {data_path}")
    dump(data, data_path)


if __name__ == "__main__":
    batch()
