# -*- coding: utf-8 -*-
from flask import request, current_app, Response, send_file
from tempfile import TemporaryFile
from test.demo.service import base_service
from flask_ssm.vo import CommonResult
from flask_ssm.springframework.web.bind.annotation import RequestMethod, RequestMapping, ExceptionHandler


# TODO 对该模块内的异常进行全局处理，可自定义修改
@ExceptionHandler(Exception)
def custom_error_handler(e: Exception) -> Response:
    current_app.logger.exception(e)
    return CommonResult.failed(message=str(e), data=e)


# TODO 自定义接口，restful风格
@RequestMapping("/hello_world", [RequestMethod.POST])
def hello_world() -> Response:
    """
    自定义接口\n
    :return: 响应
    """
    param = request.json.get("param")
    result = base_service.run(param)
    return CommonResult.ok(data=result)


# TODO 自定义接口，文件处理相关
@RequestMapping("/upload", [RequestMethod.POST])
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