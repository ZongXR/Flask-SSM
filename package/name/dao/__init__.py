# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def init_db(app: Flask):
    """
    初始化数据库配置\n
    :param app:
    :return:
    """
    db.init_app(app)
    app.logger.info("连接数据库成功")