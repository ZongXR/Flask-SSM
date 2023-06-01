# -*- coding: utf-8 -*-
from typing import Type
from functools import wraps
from flask import current_app
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

