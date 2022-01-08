# -*- coding: utf-8 -*-
from flask import Flask, Blueprint
from package.name.utils.DirUtils import recurse_files
import os


_path_ = os.getcwd()


bp = Blueprint("blue_print", __name__, static_folder=_path_ + "/static", template_folder=_path_ + "/templates", static_url_path="")


def init_view(app: Flask):
    """
    初始化view层
    :param app:
    :return:
    """
    app.register_blueprint(bp)


for file in os.listdir(os.path.dirname(__file__)):
    if file.startswith("__"):
        continue
    full_file = os.path.join(os.path.dirname(__file__), file)
    if os.path.isfile(full_file):
        module_name = file[:-3]
        __import__(__name__ + "." + module_name)
    else:
        files = recurse_files(full_file)
        for sub_file in files:
            module_name = os.path.basename(sub_file)
            path_name = os.path.dirname(sub_file)
            if module_name.startswith("__"):
                continue
            package_name = __name__ + path_name.replace(os.path.dirname(__file__), "").replace(os.sep, ".")
            if "__" in package_name:
                continue
            module_name = module_name[:-3]
            __import__(package_name + "." + module_name)

