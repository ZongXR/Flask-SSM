# -*- coding: utf-8 -*-
from typing import Type
from functools import wraps
import inspect
from flask import current_app


class Transactional:
    """
    事务管理器\n
    """
    def __init__(self, rollback_for: Type = Exception):
        """
        构造方法\n
        :param rollback_for: 捕获的异常
        """
        self.rollback_for = rollback_for

    def __call__(self, func):
        """
        执行函数\n
        :param func: 原函数
        :return:
        """
        if not issubclass(self.rollback_for, Exception):
            raise TypeError("%s is not subclass of Exception" % str(self.rollback_for))

        @wraps(func)
        def wrapper(*args, **kwargs):
            _module_ = inspect.getmodule(func)
            db = getattr(_module_, "__orm__")
            try:
                db.session.begin()
                result = func(*args, **kwargs)
            except self.rollback_for as e:
                db.session.rollback()
                current_app.logger.exception(e)
                return None
            else:
                db.session.commit()
                return result
            finally:
                db.session.close()
        return wrapper
