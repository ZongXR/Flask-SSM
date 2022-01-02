# -*- coding: utf-8 -*-
from package.name.dao import db


class BaseService:

    def __init__(self, _db=db):
        """
        构造方法\n
        """
        self._db = _db
        # self._db.create_all()

    def run(self, param) -> str:
        """
        业务逻辑\n
        :param param 参数
        :return: 答案
        """
        # TODO 在此写业务逻辑
        return str(self) + str(param)
