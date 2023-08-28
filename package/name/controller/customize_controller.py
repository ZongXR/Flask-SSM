# -*- coding: utf-8 -*-
import os
from flask import request, current_app, Response, Blueprint, send_file
from tempfile import TemporaryFile
from package.name.service import base_service
from package.name.vo import CommonResult


# 自动注册蓝图，此行代码不要动
bp = Blueprint(__name__.replace(".", "_"), __name__, static_folder="static", template_folder="templates", static_url_path="", root_path=os.getcwd())


# TODO 对该模块内的异常进行全局处理，可自定义修改
@bp.errorhandler(Exception)
def custom_error_handler(e: Exception) -> Response:
    current_app.logger.exception(e)
    return CommonResult.failed(message=str(e), data=e)


# TODO 自定义接口，restful风格
@bp.route("/hello_world", methods=["POST"])
def hello_world() -> Response:
    """
    自定义接口\n
    :return: 响应
    """
    param = request.json.get("param")
    result = base_service.run(param)
    return CommonResult.ok(data=result)


# TODO 自定义接口，文件处理相关
@bp.route("/upload", methods=["POST"])
def upload() -> Response:
    """
    上传文件\n
    :return: 响应
    """
    file = request.files.get("upload_file")
    result = TemporaryFile()
    result.write(file.stream.read())
    result.seek(0)
    return send_file(result, mimetype=file.mimetype, as_attachment=True, download_name=file.filename, attachment_filename=file.filename)