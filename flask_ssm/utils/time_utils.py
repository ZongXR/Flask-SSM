# -*- coding: utf-8 -*-
from time import time
from types import FunctionType
from typing import Tuple, Any


def execute_time(func: FunctionType, *args, **kwargs) -> Tuple[Any, int]:
    """
    执行函数并统计用时多少毫秒\n
    :param func: 要执行的函数
    :param args: 可变长度参数
    :param kwargs: 关键字参数
    :return: (原函数返回结果, 执行毫秒数)
    """
    start_time = int(round(time() * 1000))
    result = func(*args, **kwargs)
    end_time = int(round(time() * 1000))
    return result, end_time - start_time
