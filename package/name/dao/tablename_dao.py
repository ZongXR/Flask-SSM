# -*- coding: utf-8 -*-
from typing import Tuple, List
from sqlalchemy.sql.sqltypes import DECIMAL
from package.name.decorator.pybatis import mapper
from package.name.pojo.TableName import TableName


# TODO 从这以下写自己的SQL执行语句
@mapper(result_type=DECIMAL)
def query_one(user_id: int):
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
    return sql


@mapper(result_type=List[TableName])
def query_many(user_ids: Tuple[int]):
    """
    查询指定user_id范围内的pojo\n
    :param user_ids: user_id的元组
    :return: pojo的列表
    """
    sql = """
        select *
        from table_name
        where user_id in :user_ids;
    """
    return sql
