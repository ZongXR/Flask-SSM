# -*- coding: utf-8 -*-
from sqlalchemy.sql.sqltypes import *
from sqlalchemy.sql.schema import Column
from flask_ssm.pybatis.annotation import TableName


# TODO 自定义的ORM映射对象，属性与字段需对应
@TableName("table_name")
class Pojo:

    user_id = Column(INTEGER, primary_key=True)

    teach_time = Column(DECIMAL(precision=2, scale=0))

