# -*- coding: utf-8 -*-
import re
from functools import wraps
from typing import Union, Collection, Type
import inspect
from urllib.parse import unquote
from flask import request, jsonify, Response
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
        self.rule = re.sub(r'\{([^}]+)\}', r'<\1>', value)
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
                kwargs.update(request.json)
            elif request.mimetype.startswith("application/x-www-form-urlencoded") or request.mimetype.startswith("multipart/form-data"):
                values = request.values
                values = dict(zip(values.keys(), map(lambda x: unquote(x), values.values())))
                kwargs.update(values)
                if request.mimetype.startswith("multipart/form-data"):
                    kwargs.update(request.files)
            kwargs.update(dict(zip(inspect.signature(func).parameters.keys(), args)))
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


class ResponseBody:
    """
    把函数返回值的json写入响应体\n
    """
    def __init__(self, func):
        """
        构造函数\n
        :param func: 装饰的函数
        """
        wraps(func)(self)
        self.func = func

    def __call__(self, *args, **kwargs) -> Response:
        """
        调用函数\n
        :param args: 变长参数
        :param kwargs: 关键字参数
        :return: 修改后的返回值
        """
        result = self.func(*args, **kwargs)
        if type(result) is Response:
            return result
        elif issubclass(type(result), dict):
            return jsonify(dict(result))
        else:
            return jsonify(result.__dict__)