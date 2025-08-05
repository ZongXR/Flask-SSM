# -*- coding: utf-8 -*-
import inspect
from types import FunctionType
from functools import wraps
from flask import Flask, has_app_context, current_app
from flask_sqlalchemy import SQLAlchemy


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


def get_sqlalchemy() -> SQLAlchemy:
    """
    获取SQLalchemy对象\n
    :return: SQLalchemy对象, 没找到返回空
    """
    if has_app_context():
        if "sqlalchemy" in current_app.extensions.keys():
            return current_app.extensions["sqlalchemy"]
        else:
            raise ValueError("未连接数据库, 未找到绑定Flask的数据源")
    else:
        main_module = __import__("__main__")
        for _name_, _var_ in inspect.getmembers(main_module, lambda x: isinstance(x, Flask)):
            if "sqlalchemy" in _var_.extensions.keys():
                return _var_.extensions["sqlalchemy"]
        raise ValueError("未连接数据库, 未找到绑定Flask的数据源")
