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


def get_current_context(time_type:str):
    import datetime
    import time
    fmt = '%Y-%m-%d %H:%M:%S.%f' if time_type == 'datetime' else '%Y-%m-%d %H:%M:%S'
    current_time = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')



class CurrentContextTool(BaseTool):
    pass
    

    