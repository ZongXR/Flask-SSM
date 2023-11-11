# -*- coding: utf-8 -*-
from typing import Union, Collection, Type
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
        bp = blueprint_from_module(func)
        return bp.route(self.rule, methods=self.methods)(func)


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
