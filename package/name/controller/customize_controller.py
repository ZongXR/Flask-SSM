# -*- coding: utf-8 -*-
import os
from flask import request, current_app, Response, Blueprint, send_file
from package.name.service import base_service
from package.name.vo import CommonResult


# 自动注册蓝图，此行代码不要动
bp = Blueprint(__name__.replace(".", "_"), __name__, static_folder="static", template_folder="templates", static_url_path="", root_path=os.getcwd())


# TODO 在这里写自己的异常处理handler
@bp.errorhandler(Exception)
def custom_error_handler(e: Exception) -> Response:
    current_app.logger.exception(e)
    return CommonResult.failed(message=str(e), data=e)


# TODO 从这以下写自己的接口
@bp.route("/hello_world", methods=["POST"])
def hello_world() -> Response:
    """
    自定义接口\n
    :return: 响应
    """
    param = request.json.get("param")
    result = base_service.run(param)
    return CommonResult.ok(data=result)


@bp.route("/upload", methods=["POST"])
def upload() -> Response:
    """
    上传文件\n
    :return: 响应
    """
    file = request.files.get("upload_file")
    file.save(os.path.join(bp.static_folder, file.filename))
    return send_file(os.path.join(bp.static_folder, file.filename), mimetype=file.mimetype, as_attachment=True, download_name=file.filename, attachment_filename=file.filename)