DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'username'
PASSWORD = 'password'
HOST = 'localhost'
PORT = '3306'
DATABASE = 'dbname'
SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = True

