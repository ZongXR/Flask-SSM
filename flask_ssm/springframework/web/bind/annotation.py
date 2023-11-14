# -*- coding: utf-8 -*-
from functools import wraps
from typing import Union, Collection, Type
import inspect
from urllib.parse import unquote
from flask import request
from flask_ssm.utils.module_utils import blueprint_from_module


class RequestMethod:
    """
    请求方法\n
    """
    GET = "GET"
    HEAD = "HEAD"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    OPTIONS = "OPTIONS"
    TRACE = "TRACE"


class RequestMapping:
    """
    用它修饰请求接口函数\n
    """
    def __init__(self, value: str, method: Union[str, Collection[str]]):
        """
        构造方法\n
        :param value: 请求路径
        :param method: 请求方法
        """
        self.rule = value
        if type(method) is str:
            self.methods = [method]
        else:
            self.methods = list(method)

    def __call__(self, func):
        """
        执行函数\n
        :param func: 原函数
        :return:
        """
        @wraps(func)
        def result(*args, **kwargs):
            if request.mimetype.startswith("application/json"):
                kwargs = dict(**kwargs, **request.json)
            elif request.mimetype.startswith("application/x-www-form-urlencoded") or request.mimetype.startswith("multipart/form-data"):
                values = request.values
                values = dict(zip(values.keys(), map(lambda x: unquote(x), values.values())))
                kwargs = dict(**kwargs, **values)
                if request.mimetype.startswith("multipart/form-data"):
                    kwargs = dict(**kwargs, **request.files)
            kwargs = dict(**dict(zip(inspect.signature(func).parameters.keys(), args)), **kwargs)
            return func(**kwargs)
        bp = blueprint_from_module(func)
        return bp.route(self.rule, methods=self.methods)(result)


class GetMapping(RequestMapping):
    """
    用它修饰GET请求接口函数\n
    """
    def __init__(self, value: str):
        """
        构造方法\n
        :param value: 请求路径
        """
        super().__init__(value, RequestMethod.GET)

    def __call__(self, func):
        """
        执行函数\n
        :param func: 原函数
        :return:
        """
        return super().__call__(func)


class PostMapping(RequestMapping):
    """
    用它修饰POST请求接口函数\n
    """
    def __init__(self, value: str):
        """
        构造方法\n
        :param value: 请求路径
        """
        super().__init__(value, RequestMethod.POST)

    def __call__(self, func):
        """
        执行函数\n
        :param func: 原函数
        :return:
        """
        return super().__call__(func)


class ExceptionHandler:
    """
    用来统一处理同一个模块的接口异常\n
    """
    def __init__(self, value: Type[Exception] = Exception):
        """
        构造方法\n
        :param value: 捕获的异常
        """
        self.exception_cls = value

    def __call__(self, func):
        """
        执行函数\n
        :param func: 原函数
        :return:
        """
        bp = blueprint_from_module(func)
        return bp.errorhandler(self.exception_cls)(func)
