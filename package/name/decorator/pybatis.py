# -*- coding: utf-8 -*-
import sys
import typing
from typing import Type, List, Tuple, Dict, Union, Optional
from types import ModuleType
from functools import wraps
from inspect import signature
from flask import current_app
from sqlalchemy import text
from sqlalchemy.engine.cursor import CursorResult
from sqlalchemy.engine.result import MappingResult
from package.name.dao import db


if sys.version_info >= (3, 9):
    from types import GenericAlias
else:
    GenericAlias = getattr(typing, "_GenericAlias")
if sys.version_info >= (3, 8):
    from typing import get_args, get_origin
else:
    from typing_inspect import get_args, get_origin


def transactional(rollback_for: Type = Exception):
    """
    事务管理器\n
    :param rollback_for: 对哪个异常类回滚
    :return: 原函数的返回值
    """
    def decorate(func):
        if not issubclass(rollback_for, Exception):
            raise TypeError("%s is not subclass of Exception" % str(rollback_for))

        @wraps(func)
        def wrapper(*args, **kwargs):
            result = None
            try:
                result = func(*args, **kwargs)
            except rollback_for as e:
                db.session.rollback()
                current_app.logger.exception(e)
            else:
                db.session.commit()
            finally:
                return result
        return wrapper
    return decorate


def __try_to_import__(module_name: str) -> Optional[ModuleType]:
    """
    根据包名导入模块\n
    :param module_name: 包名
    :return: 模块
    """
    result = None
    try:
        result = __import__(module_name)
    except ModuleNotFoundError as e:
        pass
    return result


def mapper(result_type: Union[Type, GenericAlias] = CursorResult, *arguments, **kwargs):
    """
    ORM映射\n
    :param result_type: 要返回的类型
    :param arguments: 变长参数
    :param kwargs: 关键字参数
    :return: 修改后的返回值
    """
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **params):
            sql: str = func(*args, **params)
            if not isinstance(sql, str):
                raise TypeError("error in @mapper, return result of mapper function must be a sql string.")
            for i, k in enumerate(signature(func).parameters.keys()):
                params[k] = args[i]
            # try to import modules:
            pd = __try_to_import__("pandas")
            np = __try_to_import__("numpy")
            # process all result_types
            if result_type is CursorResult:                                                 # CursorResult
                result: CursorResult = db.session.execute(sql, params)
                return result
            elif result_type is MappingResult:                                              # MappingResult
                result: CursorResult = db.session.execute(sql, params)
                return result.mappings()
            elif pd is not None and result_type is pd.DataFrame:                            # pd.DataFrame
                result: CursorResult = db.session.execute(sql, params)
                return pd.DataFrame(result.fetchall(), columns=result.mappings().keys(), *arguments, **kwargs)
            elif pd is not None and result_type is pd.Series:                               # pd.Series
                result: CursorResult = db.session.execute(sql, params)
                values = list(zip(*result.fetchall()))
                keys = list(result.mappings().keys())
                if len(keys) > 1:
                    current_app.logger.warning("found %d columns, only pick columns[0]: %s" % (len(keys), keys[0]))
                if len(values) > 0:
                    return pd.Series(values[0], name=keys[0], *arguments, **kwargs)
                else:
                    return pd.Series(values, name=keys[0], *arguments, **kwargs)
            elif np is not None and result_type is np.ndarray:                              # np.ndarray
                result: CursorResult = db.session.execute(sql, params)
                return np.array(result.fetchall(), *arguments, **kwargs)
            elif get_origin(result_type) is list:
                if result_type is List:                                                     # List
                    result: CursorResult = db.session.execute(sql, params)
                    fetch_result = result.fetchone()
                    if fetch_result is None:
                        return None
                    else:
                        return list(fetch_result)
                elif get_origin(get_args(result_type)[0]) is dict:                          # List[Dict]
                    result: CursorResult = db.session.execute(sql, params)
                    return result.mappings().all()
                elif get_origin(get_args(result_type)[0]) is tuple:                         # List[Tuple]
                    result: CursorResult = db.session.execute(sql, params)
                    return result.fetchall()
                elif get_origin(get_args(result_type)[0]) is list:                          # List[List]
                    result: CursorResult = db.session.execute(sql, params)
                    return list(map(list, result))
                else:
                    _class_ = get_args(result_type)[0]
                    if issubclass(_class_, db.Model):                                       # List[Pojo]
                        return db.session.query(_class_).from_statement(text(sql)).params(**params).all()
                    else:                                                                   # List[T]
                        result: CursorResult = db.session.execute(sql, params)
                        keys = list(result.mappings().keys())
                        if len(keys) > 1:
                            current_app.logger.warning("found %d columns, only pick columns[0]: %s" % (len(keys), keys[0]))
                        _res_ = [x[0] for x in result]
                        if len(_res_) > 0 and type(_res_[0]) is not _class_:
                            current_app.logger.warning("type of T is %s, but required result_type is %s" % (type(_res_[0]), _class_))
                        return _res_
            elif get_origin(result_type) is tuple:
                if result_type is Tuple:                                                    # Tuple
                    result: CursorResult = db.session.execute(sql, params)
                    return result.fetchone()
                elif get_origin(get_args(result_type)[0]) is dict:                          # Tuple[Dict]
                    result: CursorResult = db.session.execute(sql, params)
                    return tuple(result.mappings().all())
                elif get_origin(get_args(result_type)[0]) is tuple:                         # Tuple[Tuple]
                    result: CursorResult = db.session.execute(sql, params)
                    fetch_result = result.fetchall()
                    return tuple(fetch_result)
                elif get_origin(get_args(result_type)[0]) is list:                          # Tuple[List]
                    result: CursorResult = db.session.execute(sql, params)
                    return tuple(map(list, result))
                else:
                    _class_ = get_args(result_type)[0]
                    if issubclass(_class_, db.Model):                                       # Tuple[Pojo]
                        return tuple(db.session.query(_class_).from_statement(text(sql)).params(**params).all())
                    else:                                                                   # Tuple[T]
                        result: CursorResult = db.session.execute(sql, params)
                        keys = list(result.mappings().keys())
                        if len(keys) > 1:
                            current_app.logger.warning("found %d columns, only pick columns[0]: %s" % (len(keys), keys[0]))
                        _res_ = tuple(x[0] for x in result)
                        if len(_res_) > 0 and type(_res_[0]) is not _class_:
                            current_app.logger.warning("type of T is %s, but required result_type is %s" % (type(_res_[0]), _class_))
                        return _res_
            elif get_origin(result_type) is dict:
                if result_type is Dict:                                                     # Dict
                    result: CursorResult = db.session.execute(sql, params)
                    return result.mappings().fetchone()
                elif get_origin(get_args(result_type)[1]) is list:                          # Dict[str, List]
                    result: CursorResult = db.session.execute(sql, params)
                    values = list(map(list, list(zip(*result.fetchall()))))
                    keys = list(result.mappings().keys())
                    if len(values) > 0:
                        return dict(zip(keys, values))
                    else:
                        return {key: [] for key in keys}
                elif get_origin(get_args(result_type)[1]) is tuple:                         # Dict[str, Tuple]
                    result: CursorResult = db.session.execute(sql, params)
                    values = list(zip(*result.fetchall()))
                    keys = list(result.mappings().keys())
                    if len(values) > 0:
                        return dict(zip(keys, values))
                    else:
                        return {key: tuple() for key in keys}
                else:                                                                       # Dict[str, T]
                    result: CursorResult = db.session.execute(sql, params)
                    values = result.fetchone()
                    keys = list(result.mappings().keys())
                    if values:
                        return dict(zip(keys, values))
                    else:
                        return {key: None for key in keys}
            else:
                _class_ = result_type
                if issubclass(_class_, db.Model):                                           # Pojo
                    if len(params) == 0:
                        return db.session.query(_class_).from_statement(text(sql)).first()
                    else:
                        return db.session.query(_class_).from_statement(text(sql)).params(**params).first()
                else:                                                                       # T
                    result: CursorResult = db.session.execute(sql, params)
                    keys = list(result.mappings().keys())
                    if len(keys) > 1:
                        current_app.logger.warning("found %d fields, only pick fields[0]: %s" % (len(keys), keys[0]))
                    fetch_result = result.fetchone()
                    if fetch_result is None:
                        return None
                    else:
                        return fetch_result[0]
        return wrapper
    return decorate
