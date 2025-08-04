# -*- coding: utf-8 -*-
from urllib.parse import quote_plus


# TODO 连接数据库配置项，可自定义修改
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = True
SQLALCHEMY_BINDS = {
    "main": {
        "url": f"mysql+pymysql://{quote_plus('root')}:{quote_plus('root')}@localhost:3306/dbname?charset=utf8",
        'pool_recycle': 7200,  # 自动回收数据库连接的时长，单位秒。可用于防止长时间闲置断开数据库连接
        'pool_pre_ping': True,  # 连接先ping后用
    }
}
SQLALCHEMY_DATABASE_URI = SQLALCHEMY_BINDS["main"]["url"]
SQLALCHEMY_ENGINE_OPTIONS = {k: v for k, v in SQLALCHEMY_BINDS["main"].items() if "url" != k}
