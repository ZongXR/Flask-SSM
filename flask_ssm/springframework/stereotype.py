# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy


class Controller:
    """
    接口\n
    """
    pass


class Service:
    """
    业务逻辑\n
    """
    pass


class Repository:
    """
    数据交互\n
    """
    db = SQLAlchemy()



