# -*- coding: utf-8 -*-
from package.name.dao import db
from package.name.dao.TableNameDao import TableNameDao


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
        table_name_dao = TableNameDao()
        return str(table_name_dao.query_one(param))
