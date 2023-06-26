# -*- coding: utf-8 -*-
import os
from flask import Blueprint, current_app, render_template


# 自动注册蓝图，此行代码不要动
bp = Blueprint(__name__.replace(".", "_"), __name__, static_folder=os.path.join(os.getcwd(), "static"), template_folder=os.path.join(os.getcwd(), "templates"), static_url_path="")


@bp.route('/', methods=["GET", "POST"])
def index():
    """
    访问主页\n
    :return: 主页静态文件
    """
    return render_template("index.html", base=current_app.config.get("APPLICATION_ROOT", "/")).strip("/")
