# -*- coding: utf-8 -*-
from typing import Type, List, Tuple, Dict
from functools import wraps
from inspect import signature
from typing_inspect import get_args, get_origin
from flask import current_app
from sqlalchemy import text
from sqlalchemy.engine.cursor import CursorResult
from package.name.dao import db


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


def mapper(result_type: Type = CursorResult):
    """
    事务管理器\n
    :param result_type: 要返回的类型
    :return: 修改后的返回值
    """
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **params):
            sql: CursorResult = func(*args, **params)
            if not isinstance(sql, str):
                raise TypeError("error in @mapper, return result of mapper function must be a sql string.")
            for i, k in enumerate(signature(func).parameters.keys()):
                params[k] = args[i]
            # try to import pandas as pd
            pd = None
            try:
                pd = __import__("pandas")
            except ModuleNotFoundError as e:
                pass
            # process all result_types
            if result_type is CursorResult:                                                 # CursorResult
                result: CursorResult = db.session.execute(sql, params)
                return result
            elif pd is not None and result_type is pd.DataFrame:                            # pd.DataFrame
                result: CursorResult = db.session.execute(sql, params)
                return pd.DataFrame(result.fetchall(), columns=result.mappings().keys())
            elif pd is not None and result_type is pd.Series:                               # pd.Series
                result: CursorResult = db.session.execute(sql, params)
                values = list(zip(*result.fetchall()))
                keys = list(result.mappings().keys())
                if len(keys) > 1:
                    current_app.logger.warning("found %d columns, only pick columns[0]: %s" % (len(keys), keys[0]))
                return pd.Series(values[0], name=keys[0])
            elif get_origin(result_type) is list:
                if result_type is List:                                                     # List
                    result: CursorResult = db.session.execute(sql, params)
                    return list(result.fetchone())
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
                        if len(params) == 0:
                            return db.session.query(_class_).from_statement(text(sql)).all()
                        else:
                            return db.session.query(_class_).from_statement(text(sql)).params(**params).all()
                    else:                                                                   # List[T]
                        result: CursorResult = db.session.execute(sql, params)
                        return [x[0] for x in result]
            elif get_origin(result_type) is tuple:
                if result_type is Tuple:                                                    # Tuple
                    result: CursorResult = db.session.execute(sql, params)
                    return result.fetchone()
                elif get_origin(get_args(result_type)[0]) is dict:                          # Tuple[Dict]
                    result: CursorResult = db.session.execute(sql, params)
                    return result.mappings()
                elif get_origin(get_args(result_type)[0]) is tuple:                         # Tuple[Tuple]
                    result: CursorResult = db.session.execute(sql, params)
                    return tuple(result.fetchall())
                elif get_origin(get_args(result_type)[0]) is list:                          # Tuple[List]
                    result: CursorResult = db.session.execute(sql, params)
                    return map(list, result)
                else:
                    _class_ = get_args(result_type)[0]
                    if issubclass(_class_, db.Model):                                       # Tuple[Pojo]
                        if len(params) == 0:
                            return tuple(db.session.query(_class_).from_statement(text(sql)).all())
                        else:
                            return tuple(db.session.query(_class_).from_statement(text(sql)).params(**params).all())
                    else:                                                                   # Tuple[T]
                        result: CursorResult = db.session.execute(sql, params)
                        return (x[0] for x in result)
            elif get_origin(result_type) is dict:
                if result_type is Dict:                                                     # Dict
                    result: CursorResult = db.session.execute(sql, params)
                    return result.mappings().fetchone()
                elif get_origin(get_args(result_type)[1]) is list:                          # Dict[str, List]
                    result: CursorResult = db.session.execute(sql, params)
                    values = list(map(list, list(zip(*result.fetchall()))))
                    keys = list(result.mappings().keys())
                    return dict(zip(keys, values))
                elif get_origin(get_args(result_type)[1]) is tuple:                         # Dict[str, Tuple]
                    result: CursorResult = db.session.execute(sql, params)
                    values = list(zip(*result.fetchall()))
                    keys = list(result.mappings().keys())
                    return dict(zip(keys, values))
                else:                                                                       # Dict[str, T]
                    result: CursorResult = db.session.execute(sql, params)
                    values = result.fetchone()
                    keys = list(result.mappings().keys())
                    return dict(zip(keys, values))
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
                    return result.fetchone()[0]
        return wrapper
    return decorate
