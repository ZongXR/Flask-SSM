# -*- coding: utf-8 -*-
import os
import sys
from typing import List, Optional, Union, Tuple, Any
from types import ModuleType, FunctionType
import inspect
from flask import Blueprint


def walk_sub_modules(package: ModuleType) -> List[ModuleType]:
    """
    递归获取子模块\n
    :param package: 包
    :return: 子模块
    """
    for _path_, _folders_, _files_ in os.walk(os.path.dirname(package.__file__), topdown=True):
        for _folder_ in _folders_:
            if _folder_.startswith("__"):
                _folders_.remove(_folder_)
        _package_name_ = package.__name__ + _path_.replace(os.path.dirname(package.__file__), "").replace(os.sep, ".")
        _files_ = list(filter(lambda x: (not x.startswith("__")) and x.lower().endswith(".py"), _files_))
        _files_ = list(map(lambda x: x[0:-3], _files_))
        for _file_ in _files_:
            _module_ = __import__(_package_name_ + "." + _file_, fromlist=[_file_])
            yield _module_


def try_to_import(*module_names: str) -> Optional[ModuleType]:
    """
    根据包名导入模块\n
    :param module_names: 包名
    :return: 模块
    """
    for module_name in module_names:
        try:
            result = __import__(module_name, fromlist=module_name.split(".")[-1])
            return result
        except ModuleNotFoundError as e:
            pass
    return None


def get_package_from_path(_path_: str, return_name: bool, change_dir: bool) -> Union[str, List[str]]:
    """
    从目录获取包名\n
    :param _path_: 目录
    :param return_name: 是 返回 package.name.service；否 返回 ['package', 'name', 'service']
    :param change_dir: 是否改变路径
    :return: 包名
    """
    _path_tree_ = list()
    while os.path.exists(os.path.join(_path_, "__init__.py")):
        _path_tree_.append(os.path.basename(_path_))
        _path_ = os.path.dirname(_path_)
        if change_dir:
            os.chdir(_path_)
    _path_tree_ = _path_tree_[::-1]
    if return_name:
        return ".".join(_path_tree_)
    else:
        return _path_tree_


def find_member_from_multi_level_package(func: FunctionType, _path_tree_: List[str]) -> List[Tuple[str, Any]]:
    """
    从多级包中寻找成员。从父向子查找，找到第一组就退出\n
    :param func: 筛选函数
    :param _path_tree_: 多级包名字组成的列表，如['package', 'name', 'service']。该参数在遍历过程中被修改，最终变为找到的位置
    :return: 寻找到的成员
    """
    while True:
        _package_name_ = ".".join(_path_tree_)
        module = __import__(_package_name_, fromlist=[_package_name_.split(".")[-1]])
        sps = inspect.getmembers(module, func)
        if len(sps) > 0:
            return sps
        if len(_path_tree_) > 0:
            _path_tree_.pop()
        else:
            return list()


def blueprint_from_module(func: FunctionType) -> Blueprint:
    """
    从函数所在的模块中提取Blueprint类对象\n
    :param func: 函数
    :return: Blueprint类的对象
    """
    _module_ = inspect.getmodule(func)
    _bps_ = inspect.getmembers(_module_, lambda x: isinstance(x, Blueprint))
    if _bps_:
        result = _bps_[-1][1]
    else:
        result = Blueprint(
            _module_.__name__.replace(".", "_"),
            _module_.__name__,
            static_folder="static",
            template_folder="templates",
            static_url_path="",
            root_path=os.path.dirname(os.path.abspath(sys.argv[0]))
        )
        setattr(_module_, "__blueprint__", result)
    return result
