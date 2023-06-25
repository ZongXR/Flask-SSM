# -*- coding: utf-8 -*-
import re
from re import Pattern
import os
import logging
from argparse import ArgumentParser
import shutil
from sqlalchemy import create_engine, MetaData, Table, inspect
from sqlalchemy.ext.automap import automap_base
import package.name.config.logs_config


def replace_txt(filename: str, old: str, new: str) -> int:
    """
    文本替换\n
    :param filename: 文件名
    :param old: 要替换的内容
    :param new: 替换成的内容
    :return: 改写行数
    """
    _result_ = 0
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
    with open(filename, "w", encoding="utf-8") as f:
        for line in lines:
            if old in line:
                line = line.replace(old, new)
                _result_ = _result_ + 1
            f.write(line)
    return _result_


def to_pojo(table_name: str, dbname: str, dialect: str, _engine_) -> bool:
    """
    把数据库的表结构映射成pojo
    :param table_name: 表名
    :param dbname: 数据库名
    :param dialect: 数据库方言，默认为空
    :param _engine_:
    :return: 是否成功
    """
    try:
        _class_name_ = table_name.title().replace("_", "")
        _insp_ = inspect(_engine_)
        with open("./package/name/pojo/TableName.py", "r", encoding="utf-8") as f:
            lines = f.readlines()
        if dialect:
            lines.insert(2, "from sqlalchemy.dialects.%s.types import *\n" % dialect)
        # get the primary key
        metadata = MetaData(bind=_engine_)
        metadata.reflect(bind=_engine_, schema=dbname, only=[table_name])
        _automap_base = automap_base(metadata=metadata)
        _automap_base.prepare()
        ow = getattr(_automap_base.classes, table_name)
        primary_key = inspect(ow).primary_key[0].name
        # write .py file
        with open("./package/name/pojo/%s.py" % _class_name_, "w", encoding="utf-8") as f:
            for line in lines[0:7]:
                f.write(line)
            f.write("class %s(db.Model):\n\n" % _class_name_)
            f.write("""    __tablename__ = "%s"\n\n""" % table_name)
            for field in _insp_.get_columns(table_name, schema=dbname):
                field_name = field["name"]
                field_type = repr(field["type"])
                field_primarykey = ", primary_key=True" if field["name"] == primary_key else ""
                f.write("    %s = Column(%s%s)\n\n" % (field_name, field_type, field_primarykey))
        return True
    except Exception as _e:
        logging.exception(_e)
        return False


def move_files(from_dir: str, to_dir: str) -> int:
    """
    把一个目录下所有的文件和文件夹放到另一个目录下\n
    :param from_dir: 从哪移出
    :param to_dir: 移到哪去
    :return: 移动了多少条
    """
    _result_ = 0
    if os.path.isfile(to_dir):
        os.remove(to_dir)
    if not os.path.exists(to_dir):
        os.makedirs(to_dir)
    for _dir_ in os.listdir(from_dir):
        logging.debug("%s -> %s" % (os.path.join(from_dir, _dir_), os.path.join(to_dir, _dir_)))
        if os.path.exists(os.path.join(to_dir, _dir_)):
            if os.path.isfile(os.path.join(to_dir, _dir_)):
                os.remove(os.path.join(to_dir, _dir_))
            else:
                shutil.rmtree(os.path.join(to_dir, _dir_))
        shutil.move(os.path.join(from_dir, _dir_), to_dir)
        _result_ = _result_ + 1
    return _result_


def set_str(_old: str, _span: tuple, _inner: str) -> str:
    """
    字符串修改指定位置\n
    :param _old: 字符串
    :param _span: 范围
    :param _inner: 插入的内容
    :return: 新字符串
    """
    return "%s%s%s" % (_old[0:_span[0]], _inner, _old[_span[1]:])


def replace_with_regex(_old: str, _regex: Pattern, *_groups) -> str:
    """
    用正则表达式进行二次替换\n
    :param _old: 原始字符串
    :param _regex: 正则表达式
    :param _groups: 捕获组替换的内容
    :return: 新的字符串
    """
    search_result = re.search(_regex, _old)
    while search_result is not None:
        for k, _group in enumerate(_groups):
            if _group is None:
                continue    # 防止不必要的捕获组替换
            _old = set_str(_old, search_result.span(k + 1), _group)
        search_result = re.search(_regex, _old)
    return _old


if __name__ == '__main__':
    parser = ArgumentParser(description="initialize flask mvc framework with your own arguments")
    # add arguments
    parser.add_argument("--package-name", help="Name of the package", type=str)
    parser.add_argument("--db-dialect", help="dialect of database", type=str)
    parser.add_argument("--db-driver", help="driver of database", type=str)
    parser.add_argument("--db-username", help="username of database", type=str)
    parser.add_argument("--db-password", help="password of database", type=str)
    parser.add_argument("--db-host", help="host of database", type=str)
    parser.add_argument("--db-port", help="port of database", type=str)
    parser.add_argument("--db-database", help="name of database", type=str)
    parser.add_argument("--db-tables", help="table names in the database", dest="db_tables", nargs="+")
    parser.add_argument("--log-level", help="level of logging", type=str)
    parser.add_argument("--app-host", help="host of the app", type=str)
    parser.add_argument("--app-port", help="port of the app", type=int)
    parser.add_argument("--application-root", help="context path of the app", type=str)
    parser.add_argument("--app-debug", help="whether if the app is in debug", type=bool)
    args = parser.parse_args()

    # get argument values
    package_name = args.package_name
    log_level = args.log_level
    db_dialect = args.db_dialect
    db_driver = args.db_driver
    db_username = args.db_username
    db_password = args.db_password
    db_host = args.db_host
    db_port = args.db_port
    db_database = args.db_database
    db_tables = args.db_tables
    app_host = args.app_host
    app_port = args.app_port
    application_root = args.application_root
    app_debug = args.app_debug

    # 改写文件内容
    result = 0
    if log_level:
        logging.info("replacing log level config, set to %s" % log_level)
        try:
            result = result + replace_txt(
                "./package/name/config/logs_config.py",
                """"root": {"level": "DEBUG", "handlers": ["console", "debug", "info", "warn", "error"]}""",
                """"root": {"level": "%s", "handlers": ["console", "debug", "info", "warn", "error"]}""" % log_level
            )
        except Exception as e:
            logging.exception(e)
    if db_dialect:
        logging.info("replacing database dialect, set to %s" % db_dialect)
        try:
            result = result + replace_txt(
                "./package/name/config/database_config.py",
                """DB_DIALECT = 'mysql'""",
                """DB_DIALECT = '%s'""" % db_dialect
            )
        except Exception as e:
            logging.exception(e)
    if db_driver:
        logging.info("replacing database driver, set to %s" % db_driver)
        try:
            result = result + replace_txt(
                "./package/name/config/database_config.py",
                """DB_DRIVER = 'pymysql'""",
                """DB_DRIVER = '%s'""" % db_driver
            )
        except Exception as e:
            logging.exception(e)
    if db_username:
        logging.info("replacing database username, set to %s" % db_username)
        try:
            result = result + replace_txt(
                "./package/name/config/database_config.py",
                """DB_USERNAME = quote_plus('root')""",
                """DB_USERNAME = quote_plus('%s')""" % db_username
            )
        except Exception as e:
            logging.exception(e)
    if db_password:
        logging.info("replacing database password, set to %s" % db_password)
        try:
            result = result + replace_txt(
                "./package/name/config/database_config.py",
                """DB_PASSWORD = quote_plus('root')""",
                """DB_PASSWORD = quote_plus('%s')""" % db_password
            )
        except Exception as e:
            logging.exception(e)
    if db_host:
        logging.info("replacing database host, set to %s" % db_host)
        try:
            result = result + replace_txt(
                "./package/name/config/database_config.py",
                """DB_HOST = 'localhost'""",
                """DB_HOST = '%s'""" % db_host
            )
        except Exception as e:
            logging.exception(e)
    if db_port:
        logging.info("replacing database port, set to %s" % db_port)
        try:
            result = result + replace_txt(
                "./package/name/config/database_config.py",
                """DB_PORT = '3306'""",
                """DB_PORT = '%s'""" % db_port
            )
        except Exception as e:
            logging.exception(e)
    if db_database:
        logging.info("replacing database name, set to %s" % db_database)
        try:
            result = result + replace_txt(
                "./package/name/config/database_config.py",
                """DB_DATABASE = 'dbname'""",
                """DB_DATABASE = '%s'""" % db_database
            )
        except Exception as e:
            logging.exception(e)
    if app_host:
        logging.info("replacing the host of the app")
        try:
            result = result + replace_txt(
                "./package/name/config/app_config.py",
                """APP_HOST = '0.0.0.0'""",
                """APP_HOST = '%s'""" % app_host
            )
        except Exception as e:
            logging.exception(e)
    if app_port:
        logging.info("replacing the port of the app")
        try:
            result = result + replace_txt(
                "./package/name/config/app_config.py",
                """APP_PORT = 5000""",
                """APP_HOST = %d""" % app_port
            )
        except Exception as e:
            logging.exception(e)
    if app_debug:
        logging.info("replacing the debug flag of the app")
        try:
            result = result + replace_txt(
                "./package/name/config/app_config.py",
                """DEBUG = False""",
                """DEBUG = %s""" % app_debug
            )
        except Exception as e:
            logging.exception(e)
    if application_root:
        logging.info("set the context path of the app")
        try:
            result = result + replace_txt(
                "./package/name/config/app_config.py",
                """APPLICATION_ROOT = '/'""",
                """APPLICATION_ROOT = '%s'""" % application_root
            )
            result = result + replace_txt(
                "./static/index.html",
                """    <input id="url" placeholder="输入请求地址" type="text" value="/custom"/>""",
                """    <input id="url" placeholder="输入请求地址" type="text" value="%s/custom"/>""" % application_root.rstrip("/")
            )
        except Exception as e:
            logging.exception(e)
    if db_tables:
        if db_dialect in ["mysql", "postgresql", "mssql", "oracle", "sqlite", "sybase", "firebird"]:
            try:
                with create_engine("{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(db_dialect, db_driver, db_username, db_password, db_host, db_port, db_database)) as engine:
                    for db_table in db_tables:
                        logging.info("creating pojo with table %s" % db_table)
                        result = result + to_pojo(db_table, db_database, db_dialect, engine)
            except Exception as e:
                logging.exception(e)
        else:
            logging.warning("skip param --db-tables, only support mysql, postgresql, mssql, oracle, sqlite, sybase, firebird now.")

    if package_name and package_name != "package.name":
        try:
            # write import codes
            for _path_, _folders_, _files_ in os.walk(os.getcwd(), topdown=True):
                for _file_ in _files_:
                    if _file_.endswith(".py") or _file_.endswith(".PY"):
                        _file_path_ = os.path.join(_path_, _file_)
                        if _file_path_ == os.path.join(os.getcwd(), __file__) or _file_path_ == __file__.replace("/", os.sep):
                            continue    # skip the initializer file
                        logging.debug("read file from %s." % _file_path_)
                        with open(_file_path_, "r", encoding="utf-8") as f:
                            _file_codes_ = f.read()

                        _file_codes_new_ = replace_with_regex(_file_codes_, re.compile(r"\s*from (package\.name)(\.\S+)* import \S+\s*"), package_name)
                        _file_codes_new_ = replace_with_regex(_file_codes_new_, re.compile(r"\s*import (package\.name)(\.\S+)*\s*"), package_name)
                        if _file_codes_ is not _file_codes_new_:
                            with open(_file_path_, "w", encoding="utf-8") as f:
                                f.write(_file_codes_new_)
                                result = result + 1
            # change file path
            package_names = package_name.split(".")
            if package_name == "package":
                result = result + move_files("./package/name", "./package")
                shutil.rmtree("./package/name")
            elif package_name.startswith("package.name."):
                result = result + move_files("./package/name", os.path.join(*package_names))
            else:
                result = result + move_files("./package/name", os.path.join(*package_names))
                shutil.rmtree("./package")
            # create __init__.py
            for i, package in enumerate(package_names):
                _init_file = os.path.join(*(package_names[0:i+1] + ["__init__.py"]))
                if not os.path.exists(_init_file):
                    open(_init_file, "w", encoding="utf-8")
        except Exception as e:
            logging.exception(e)

    logging.info("已完成初始化，替换内容%d处" % result)