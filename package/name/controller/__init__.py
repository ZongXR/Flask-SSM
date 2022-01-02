# -*- coding: utf-8 -*-
from flask import Flask, Blueprint
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
    module_name = file[:-3]
    if not module_name.startswith("__"):
        __import__(__name__ + "." + module_name)
