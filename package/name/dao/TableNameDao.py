# -*- coding: utf-8 -*-
from package.name.dao import db


class TableNameDao(db.Model):

    __tablename__ = "table_name"

    user_id = db.Column(db.INT, primary_key=True)

    teach_time = db.Column(db.DECIMAL(2))


