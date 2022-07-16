# -*- coding: utf-8 -*-
from flask_sqlalchemy.model import Model
from sqlalchemy.sql.sqltypes import INT, DECIMAL
from sqlalchemy.sql.schema import Column


class TableName(Model):

    __tablename__ = "table_name"

    user_id = Column(INT, primary_key=True)

    teach_time = Column(DECIMAL(2))
