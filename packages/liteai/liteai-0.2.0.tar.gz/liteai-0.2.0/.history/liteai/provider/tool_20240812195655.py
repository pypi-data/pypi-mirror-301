#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2024/08/12 19:54:53
@Author  :   ChenHao
@Description  :   工具类
@Contact :   jerrychen1990@gmail.com
'''


from typing import Any, Callable

from litellm import Field

from liteai.core import ToolDesc


class BaseTool(ToolDesc):
    callable: Callable = Field(..., description="工具执行函数")

    def execute(self, *args, **kwargs) -> Any:
        return self.callable(*args, **kwargs)


def get_current_context():
    cur_time = import datetime
    import time
    datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')



class CurrentContextTool(BaseTool):
    pass
    

    