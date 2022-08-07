# -*- coding: utf-8 -*-
import os
from flask import Response, Blueprint, send_from_directory, current_app
from package.name.vo import CommonResult


# 自动注册蓝图，此行代码不要动
bp = Blueprint(__name__.replace(".", "_"), __name__, static_folder=os.path.join(os.getcwd(), "static"), template_folder=os.path.join(os.getcwd(), "templates"), static_url_path="")


@bp.route('/', methods=["GET", "POST"])
def index():
    """
    访问主页\n
    :return: 主页静态文件
    """
    return bp.send_static_file("index.html")


@bp.route("/favicon.ico", methods=["GET", "POST"])
def favicon() -> Response:
    """
    返回网站图标\n
    :return: 网站图标文件
    """
    return send_from_directory(
        bp.static_folder,
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon"
    )


@bp.app_errorhandler(Exception)
def error_handler(e: Exception) -> Response:
    """
    处理异常\n
    :param e: 异常
    :return: 响应
    """
    current_app.logger.exception(e)
    return CommonResult.failed(message=str(e), data=repr(e))
