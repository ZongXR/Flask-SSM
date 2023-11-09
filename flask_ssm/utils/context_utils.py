# -*- coding: utf-8 -*-
from types import FunctionType
from functools import wraps
from flask import Flask
import flask.globals as globs


def add_app_context(app: Flask, func: FunctionType) -> FunctionType:
    """
    给函数加上上下文\n
    :param app: Flask对象
    :param func: 函数
    :return: 有上下文的函数
    """
    @wraps(func)
    def result(*args, **kwargs):
        with app.app_context():
            return func(*args, **kwargs)
    return result


def has_app_context() -> bool:
    """
    判断是否有上下文\n
    :return: 是否有上下文
    """
    _app_ctx_stack = getattr(globs, "_app_ctx_stack", None)
    return _app_ctx_stack.top is not None
