# -*- coding: utf-8 -*-
from sqlalchemy.sql.sqltypes import INT, DECIMAL
from sqlalchemy.sql.schema import Column
from package.name.dao import db


class TableName(db.Model):

    __tablename__ = "table_name"

    user_id = Column(INT, primary_key=True)

    teach_time = Column(DECIMAL(2))
