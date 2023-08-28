# -*- coding: utf-8 -*-
from sqlalchemy.sql.sqltypes import *
from sqlalchemy.sql.schema import Column
from package.name.dao import db


# TODO 自定义的ORM映射对象，必须继承自db.Model，属性与字段需对应
class TableName(db.Model):

    __tablename__ = "table_name"

    user_id = Column(INTEGER, primary_key=True)

    teach_time = Column(DECIMAL(precision=2, scale=0))

