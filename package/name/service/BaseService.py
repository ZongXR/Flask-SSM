# -*- coding: utf-8 -*-
from flask import current_app
from package.name.dao import db
from package.name.dao.TableNameDao import query_one


class BaseService:

    __instance__ = None

    def __new__(cls, *args, **kwargs):
        """
        实现单例模式\n
        :param args: 变长参数
        :param kw: 关键字参数
        :return 单例对象
        """
        if cls.__instance__ is None:
            cls.__instance__ = object.__new__(cls, *args, **kwargs)
        return cls.__instance__

    def __init__(self, _db=db) -> None:
        """
        构造方法\n
        :return 空
        """
        self._db = _db

    def run(self, param: int) -> str:
        """
        业务逻辑\n
        :param param 参数
        :return: 答案
        """
        # TODO 在此写业务逻辑
        current_app.logger.info("执行业务逻辑%s, 参数%s" % (type(self), param))
        return str(query_one(param))
