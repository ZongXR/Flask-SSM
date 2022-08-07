# -*- coding: utf-8 -*-
import os
from flask import Flask
from package.name.utils.DirUtils import recurse_files


__blueprints__ = []
for _file_ in os.listdir(os.path.dirname(__file__)):
    if _file_.startswith("__"):
        continue
    _full_file_ = os.path.join(os.path.dirname(__file__), _file_)
    if os.path.isfile(_full_file_):
        _module_name_ = _file_[:-3]
        __import__(__name__ + "." + _module_name_)
        __blueprints__.append(eval(_module_name_ + ".bp"))
    else:
        _files_ = recurse_files(_full_file_)
        for _sub_file_ in _files_:
            _module_name_ = os.path.basename(_sub_file_)
            _path_name_ = os.path.dirname(_sub_file_)
            if _module_name_.startswith("__"):
                continue
            _package_name_ = __name__ + _path_name_.replace(os.path.dirname(__file__), "").replace(os.sep, ".")
            if "__" in _package_name_:
                continue
            _module_name_ = _module_name_[:-3]
            __import__(_package_name_ + "." + _module_name_)
            __blueprints__.append(eval(_module_name_ + ".bp"))


def init_view(app: Flask):
    """
    初始化view层
    :param app:
    :return:
    """
    for __blueprint__ in __blueprints__:
        app.register_blueprint(__blueprint__)
    app.logger.info("初始化view成功")
