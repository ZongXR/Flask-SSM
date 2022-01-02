# -*- coding: utf-8 -*-
from flask import Response, send_from_directory
from package.name.controller import bp


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