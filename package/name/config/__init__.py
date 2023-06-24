# -*- coding: utf-8 -*-
import os
from typing import List
from types import ModuleType
from flask import Flask


__modules__: List[ModuleType] = []
for _path_, _folders_, _files_ in os.walk(os.path.dirname(__file__), topdown=True):
    for _folder_ in _folders_:
        if _folder_.startswith("__"):
            _folders_.remove(_folder_)
    _package_name_ = __name__ + _path_.replace(os.path.dirname(__file__), "").replace(os.sep, ".")
    _files_ = list(filter(lambda x: not x.startswith("__"), _files_))
    _files_ = list(map(lambda x: x[0:-3], _files_))
    for _file_ in _files_:
        _module_ = __import__(_package_name_ + "." + _file_, fromlist=[_file_])
        __modules__.append(_module_)


def init_config(app: Flask):
    """
    初始化view层
    :param app:
    :return:
    """
    for __module__ in __modules__:
        app.config.from_object(__module__)
    if app.config.get("EUREKA_ENABLED", None):
        try:
            flask_eureka = __import__("flask_eureka")
        except ModuleNotFoundError as e:
            app.logger.exception(e)
        else:
            eureka = flask_eureka.Eureka(app)
            eureka.register_service()
            app.register_blueprint(flask_eureka.eureka.eureka_bp)
    app.logger.info("初始化配置成功")
