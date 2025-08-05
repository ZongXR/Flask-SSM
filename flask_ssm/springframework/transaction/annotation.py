# -*- coding: utf-8 -*-
from enum import IntEnum
from typing import Type, Callable
from functools import wraps
import inspect
from sqlalchemy.orm import scoped_session
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from flask_ssm.springframework.transaction import IllegalTransactionStateException
from flask_ssm.utils.context_utils import get_sqlalchemy


class Isolation(IntEnum):
    """
    事务隔离级别\n
    """
    DEFAULT = -1,
    READ_UNCOMMITTED = 1,
    READ_COMMITTED = 2,
    REPEATABLE_READ = 4,
    SERIALIZABLE = 8


class Propagation(IntEnum):
    """
    事务传播级别\n
    """
    REQUIRED = 0,
    SUPPORTS = 1,
    MANDATORY = 2,
    REQUIRES_NEW = 3,
    NOT_SUPPORTED = 4,
    NEVER = 5,
    NESTED = 6


class Transactional:
    """
    事务管理器\n
    """
    def __init__(self, propagation: Propagation = Propagation.REQUIRED, rollback_for: Type = Exception):
        """
        构造方法\n
        :param propagation: 事务传播机制
        :param rollback_for: 捕获的异常
        """
        self.propagation = propagation
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
            db: SQLAlchemy = get_sqlalchemy()
            in_transaction = db.session().in_transaction()
            if self.propagation is Propagation.REQUIRED:
                if in_transaction:
                    return func(*args, **kwargs)
                else:
                    return self.__start_transaction__(func, db.session, *args, **kwargs)
            elif self.propagation is Propagation.SUPPORTS:
                return func(*args, **kwargs)
            elif self.propagation is Propagation.MANDATORY:
                if in_transaction:
                    return func(*args, **kwargs)
                else:
                    raise IllegalTransactionStateException(f"No existing transaction found for transaction marked with propagation '{self.propagation}'")
            elif self.propagation is Propagation.REQUIRES_NEW:
                if in_transaction:
                    secondary_session = scoped_session(
                        db.session.session_factory,
                        scopefunc=db.session.registry.scopefunc
                    )
                    db_session = db.session
                    try:
                        db.session = secondary_session
                        return self.__start_transaction__(func, db.session, *args, **kwargs)
                    finally:
                        db.session = db_session
                        secondary_session.remove()
                else:
                    return self.__start_transaction__(func, db.session, *args, **kwargs)
            elif self.propagation is Propagation.NOT_SUPPORTED:
                if in_transaction:
                    secondary_session = scoped_session(
                        db.session.session_factory,
                        scopefunc=db.session.registry.scopefunc
                    )
                    db_session = db.session
                    try:
                        db.session = secondary_session
                        return func(*args, **kwargs)
                    finally:
                        db.session = db_session
                        secondary_session.remove()
                else:
                    return func(*args, **kwargs)
            elif self.propagation is Propagation.NEVER:
                if in_transaction:
                    raise IllegalTransactionStateException(f"Existing transaction found for transaction marked with propagation '{self.propagation}'")
                else:
                    return func(*args, **kwargs)
            elif self.propagation is Propagation.NESTED:
                if in_transaction:
                    return self.__start_transaction__(func, db.session, True, *args, **kwargs)
                else:
                    return self.__start_transaction__(func, db.session, *args, **kwargs)
            else:
                raise ValueError(f"Unknown parameter propagation={self.propagation}")
        return wrapper

    def __start_transaction__(self, func: Callable, session: scoped_session, nested: bool = False, *args, **kwargs):
        """
        开始一个事务\n
        :param func: 执行的函数
        :param session: 会话
        :param nested: 是否嵌套事务
        :param args: func的可变长度参数
        :param kwargs: func的关键字参数
        """
        savepoint = session.begin(nested=nested)
        try:
            result = func(*args, **kwargs)
        except self.rollback_for as e:
            if nested:
                savepoint.rollback()
            else:
                session.rollback()
            current_app.logger.exception(e)
            raise e
        else:
            if nested:
                savepoint.commit()
            else:
                session.flush()
                session.commit()
            return result
        finally:
            if not nested and session is not None:
                session.close()

