# -*- coding: utf-8 -*-
import os
import inspect
from typing import List
from flask import Flask, Blueprint


__blueprints__: List[Blueprint] = []
for _path_, _folders_, _files_ in os.walk(os.path.dirname(__file__), topdown=True):
    for _folder_ in _folders_:
        if _folder_.startswith("__"):
            _folders_.remove(_folder_)
    _package_name_ = __name__ + _path_.replace(os.path.dirname(__file__), "").replace(os.sep, ".")
    _files_ = list(filter(lambda x: not x.startswith("__"), _files_))
    _files_ = list(map(lambda x: x[0:-3], _files_))
    for _file_ in _files_:
        _module_ = __import__(_package_name_ + "." + _file_, fromlist=[_file_])
        _bps_ = inspect.getmembers(_module_, lambda x: isinstance(x, Blueprint))
        __blueprints__.extend(list(map(lambda x: x[1], _bps_)))


def init_view(app: Flask):
    """
    初始化view层
    :param app:
    :return:
    """
    for __blueprint__ in __blueprints__:
        app.register_blueprint(__blueprint__, url_prefix=app.config.get("APPLICATION_ROOT", ""))
    app.logger.info("初始化view成功")
