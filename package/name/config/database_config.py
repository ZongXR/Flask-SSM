# -*- coding: utf-8 -*-
from urllib.parse import quote_plus


db_dialect = 'mysql'
db_driver = 'pymysql'
db_username = quote_plus('root')
db_password = quote_plus('root')
db_host = 'localhost'
db_port = '3306'
db_database = 'dbname'
SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(db_dialect, db_driver, db_username, db_password, db_host, db_port, db_database)
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = True
