# -*- coding: utf-8 -*-
from typing import List
from flask import current_app
from package.name.dao import tablename_dao
from package.name.pojo.TableName import TableName
from package.name.decorator.unittest import test


# TODO 在此写业务逻辑
def run(param: int) -> str:
    """
    业务逻辑\n
    :param param 参数
    :return: 答案
    """
    current_app.logger.info("执行业务逻辑, 参数%s" % param)
    result = tablename_dao.query_one(param)
    return str(result)


# TODO 在此写单元测试
@test
def test_method(user_ids: List[int]) -> List[TableName]:
    """
    单元测试\n
    :param user_ids: user_id列表
    :return: pojo列表
    """
    return tablename_dao.query_many(tuple(user_ids))


if __name__ == '__main__':
    print(test_method([1, 2]))
