# -*- coding: utf-8 -*-
import os
from flask import Flask, Blueprint


def __recurse_files__(path: str) -> [str]:
    """
    递归查询目录下所有文件\n
    :param path: 目录
    :return: 目录树
    """
    result = []
    if os.path.isfile(path):
        result.append(path)
    else:
        files = os.listdir(path)
        paths = map(lambda x: os.path.join(path, x), files)
        for path_one in paths:
            if not os.path.dirname(path_one).split(os.path.sep)[-1].startswith("__"):
                result.extend(__recurse_files__(path_one))
    return result


__blueprints__ = []
for _file_ in os.listdir(os.path.dirname(__file__)):
    if _file_.startswith("__"):
        continue
    _full_file_ = os.path.join(os.path.dirname(__file__), _file_)
    if os.path.isfile(_full_file_):
        _module_name_ = _file_[:-3]
        _module_ = __import__(__name__ + "." + _module_name_, fromlist=[_module_name_])
        _bps_ = list(filter(lambda x: isinstance(eval(_module_name_ + "." + x), Blueprint), dir(_module_)))
        __blueprints__.extend(list(map(lambda x: eval(_module_name_ + "." + x), _bps_)))
    else:
        _files_ = __recurse_files__(_full_file_)
        for _sub_file_ in _files_:
            _module_name_ = os.path.basename(_sub_file_)
            _path_name_ = os.path.dirname(_sub_file_)
            if _module_name_.startswith("__"):
                continue
            _package_name_ = __name__ + _path_name_.replace(os.path.dirname(__file__), "").replace(os.sep, ".")
            _module_name_ = _module_name_[:-3]
            exec("from %s import %s" % (_package_name_, _module_name_))
            _module_ = __import__(_package_name_ + "." + _module_name_, fromlist=[_module_name_])
            _bps_ = list(filter(lambda x: isinstance(eval(_module_name_ + "." + x), Blueprint), dir(_module_)))
            __blueprints__.extend(list(map(lambda x: eval(_module_name_ + "." + x), _bps_)))


def init_view(app: Flask):
    """
    初始化view层
    :param app:
    :return:
    """
    for __blueprint__ in __blueprints__:
        app.register_blueprint(__blueprint__)
    app.logger.info("初始化view成功")
