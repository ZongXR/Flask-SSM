# -*- coding: utf-8 -*-
import sys
from typing import Type
from flask import Response, jsonify


if sys.version_info >= (3, 8):
    from typing import get_origin
else:
    from typing_inspect import get_origin


def __get_origin__(tp):
    """
    对系统get_origin的扩展\n
    :param tp: 输入类型
    :return: 返回get_origin的类型或原类型
    """
    _result_ = get_origin(tp)
    return tp if _result_ is None else _result_


def pojo_private_properties(cls: Type) -> dict:
    """
    获取pojo类的私有属性\n
    :param cls: pojo类
    :return: 属性字典
    """
    result = dict()
    if hasattr(cls, "__tablename__"):
        result["__tablename__"] = getattr(cls, "__tablename__")
    if hasattr(cls, "__table__"):
        result["__table__"] = getattr(cls, "__table__")
    if hasattr(cls, "__bind_key__"):
        result["__bind_key__"] = getattr(cls, "__bind_key__")
    if hasattr(cls, "__table_args__"):
        result["__table_args__ "] = getattr(cls, "__table_args__")
    return result


def to_json(obj) -> Response:
    """
    把obj转为json串\n
    :param obj: 要转换的对象
    :return: 响应
    """
    if type(obj) is Response:
        return obj
    elif issubclass(type(obj), dict):
        return jsonify(dict(obj))
    else:
        return jsonify(obj.__dict__)
