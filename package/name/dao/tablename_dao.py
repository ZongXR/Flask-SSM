# -*- coding: utf-8 -*-
from sqlalchemy.sql.sqltypes import DECIMAL
from package.name.dao import db


def query_one(user_id: int) -> DECIMAL:
    """
    获取该表某一行数据\n
    :param user_id: 用户编号
    :return: 全部数据
    """
    sql = """
        select teach_time
        from table_name
        where user_id = :user_id;
    """
    return list(db.session.execute(sql, {"user_id": user_id}))[0][0]
