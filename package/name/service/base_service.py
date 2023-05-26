# -*- coding: utf-8 -*-
from flask import current_app
from package.name.dao import db
from package.name.dao import tablename_dao


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
