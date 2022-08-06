# -*- coding: utf-8 -*-
from flask import Response, send_from_directory
from package.name.controller import bp_base
from package.name.vo import CommonResult


@bp_base.route('/', methods=["GET", "POST"])
def index():
    """
    访问主页\n
    :return: 主页静态文件
    """
    return bp_base.send_static_file("index.html")


@bp_base.route("/favicon.ico", methods=["GET", "POST"])
def favicon() -> Response:
    """
    返回网站图标\n
    :return: 网站图标文件
    """
    return send_from_directory(
        bp_base.static_folder,
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon"
    )


@bp_base.app_errorhandler(Exception)
def error_handler(e: Exception) -> Response:
    """
    处理异常\n
    :param e: 异常
    :return: 响应
    """
    return CommonResult.failed(message=str(e), data=repr(e))
