# -*- coding: utf-8 -*-
from flask_ssm.pybatis.annotation import Mapper


# TODO 从这以下写自己的SQL执行语句
@Mapper(result_type=str)
def query_one(param: str):
    """
    获取一个字段\n
    :param param: 输入参数
    :return: 全部数据
    """
    sql = """
        select :param;
    """
    return sql
