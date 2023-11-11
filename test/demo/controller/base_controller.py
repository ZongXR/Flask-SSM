# -*- coding: utf-8 -*-
from flask import current_app, render_template
from flask_ssm.springframework.web.bind.annotation import RequestMapping
from flask_ssm.springframework.web.bind.annotation import RequestMethod


@RequestMapping("/", [RequestMethod.GET, RequestMethod.POST])
def index():
    """
    访问主页\n
    :return: 主页静态文件
    """
    base_path = current_app.config.get("APPLICATION_ROOT", "/")
    base_path = "" if base_path == "/" else "/" + base_path.strip("/")
    return render_template("index.html", base=base_path)
