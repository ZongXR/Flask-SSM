# -*- coding: utf-8 -*-
from flask import current_app
from flask_ssm.unittest import Test
from test.demo.dao import tablename_dao


# TODO 在此写业务逻辑，如果需要进行单元测试，直接加上 @Test
@Test
def run(param: str) -> str:
    """
    业务逻辑\n
    :param param 参数
    :return: 答案
    """
    current_app.logger.info("执行业务逻辑, 参数: '%s'" % param)
    result = tablename_dao.query_one(param)
    return str(result)


if __name__ == '__main__':
    print(run("Hello World"))
