# -*- coding: utf-8 -*-
from urllib.parse import quote_plus


# TODO 连接数据库配置项，可自定义修改
db_dialect = 'mysql'                 # 数据库方言
db_driver = 'pymysql'                # 数据库驱动
db_username = quote_plus('root')     # 用户名
db_password = quote_plus('root')     # 密码
db_host = 'localhost'                # 数据库地址
db_port = '3306'                     # 数据库端口
db_database = 'dbname'               # 数据库名称
SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(db_dialect, db_driver, db_username, db_password, db_host, db_port, db_database)
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = True
SQLALCHEMY_POOL_RECYCLE = 7200       # 自动回收数据库连接的时长，单位秒。可用于防止长时间闲置断开数据库连接
