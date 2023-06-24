# -*- coding: utf-8 -*-
from urllib.parse import quote_plus


DB_DIALECT = 'mysql'
DB_DRIVER = 'pymysql'
DB_USERNAME = quote_plus('root')
DB_PASSWORD = quote_plus('root')
DB_HOST = 'localhost'
DB_PORT = '3306'
DB_DATABASE = 'dbname'
SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DB_DIALECT, DB_DRIVER, DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = True

