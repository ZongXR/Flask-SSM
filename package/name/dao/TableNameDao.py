# -*- coding: utf-8 -*-
from package.name.dao import db


class TableNameDao(db.Model):

    __tablename__ = "table_name"

    user_id = db.Column(db.INT, primary_key=True)

    teach_time = db.Column(db.DECIMAL(2))

    def query_one(self, user_id: int) -> db.DECIMAL:
        """
        获取该表某一行数据\n
        :param user_id: 用户编号
        :return: 全部数据
        """
        sql = """
            select teach_time
            from %s
            where user_id = :user_id;
        """ % self.__tablename__
        return list(db.session.execute(sql, {"user_id": user_id}))[0][0]
