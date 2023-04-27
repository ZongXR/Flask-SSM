# -*- coding: utf-8 -*-
from typing import Type
from flask import current_app
from package.name.dao import db


def transactional(func, rollback_for: Type = Exception):
    """
    事务管理器\n
    :param func: 加事务的函数
    :param rollback_for: 对哪个异常类回滚
    :return: 原函数的返回值
    """
    if not issubclass(rollback_for, Exception):
        current_app.logger.exception("%s is not subclass of Exception" % str(rollback_for))
        return func

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
