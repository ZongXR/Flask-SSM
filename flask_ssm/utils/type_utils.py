# -*- coding: utf-8 -*-
import sys
import logging
import json
import inspect
from inspect import Parameter
from typing import Type, Tuple
from types import FunctionType
from pydantic import create_model, ValidationError, TypeAdapter


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


def to_json(obj) -> str:
    """
    把obj转为json串\n
    :param obj: 要转换的对象
    :return: 响应
    """
    if type(obj) is str:
        return f'"{obj}"'
    elif issubclass(type(obj), dict):
        return json.dumps(dict(obj))
    elif hasattr(obj, "__dict__"):
        return json.dumps(obj.__dict__)
    else:
        return str(obj)


def validate_value_with_type(value_type, value):
    """
    验证value是否符合value_type\n
    :param value_type: 参数类型
    :param value: 数值
    :return: 验证或转换类型后的value
    """
    model = create_model('DynamicModel', value=(value_type, ...))
    validated_value = model(value=value)
    return validated_value.value


def validate_single_value(value_type, value):
    """
    验证某一个value的类型\n
    :param value_type: 参数类型
    :param value: 数值
    :return: 验证或转换类型后的value
    """
    try:
        return validate_value_with_type(value_type, value)
    except ValidationError as e:
        logging.warning(e)
        return value


def function_parameter_defaults(func):
    """
    过去函数参数默认值\n
    :param func: 函数
    :return: 默认值组成的字典
    """
    sig = inspect.signature(func)
    defaults = {}
    for name, param in sig.parameters.items():
        if param.default is not Parameter.empty:
            defaults[name] = param.default
    return defaults


def validate_function(func: FunctionType, kwargs: dict) -> Tuple[dict, dict]:
    """
    验证函数的参数是否符合类型\n
    :param func: 函数
    :param kwargs: 函数的实参
    :return: 已验证的, 未验证的
    """
    errors = dict()
    validated = dict()
    function_defaults = function_parameter_defaults(func)
    for _name_, _type_ in func.__annotations__.items():
        if "return" == _name_:
            continue
        _input_ = kwargs.get(_name_)
        try:
            adapter = TypeAdapter(_type_)
            validated[_name_] = adapter.validate_python(_input_)
        except ValidationError as e:
            if _input_ is None and _name_ in function_defaults.keys():
                try:
                    validated[_name_] = validate_value_with_type(_type_, function_defaults[_name_])
                except ValidationError as e:
                    err = e.errors()[0]
                    errors[_name_] = err
            else:
                err = e.errors()[0]
                errors[_name_] = err
    kwargs = {**kwargs, **validated}
    return kwargs, errors
