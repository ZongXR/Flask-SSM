# -*- coding: utf-8 -*-
from sqlalchemy.sql.sqltypes import *
from sqlalchemy.dialects.mysql.types import *
from sqlalchemy.sql.schema import Column
from package.name.dao import db


class TableName(db.Model):

    __tablename__ = "table_name"

    user_id = Column(INTEGER(display_width=11), primary_key=True)

    teach_time = Column(DECIMAL(precision=2, scale=0))

