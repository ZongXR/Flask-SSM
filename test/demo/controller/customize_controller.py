# -*- coding: utf-8 -*-
from flask import current_app, Response, send_file
from tempfile import TemporaryFile
from test.demo.service import base_service
from flask_ssm.vo import CommonResult
from flask_ssm.springframework.web.bind.annotation import RequestMethod, RequestMapping, ExceptionHandler, ResponseBody


# TODO 对该模块内的异常进行全局处理，可自定义修改
@ExceptionHandler(Exception)
@ResponseBody
def custom_error_handler(e: Exception) -> CommonResult:
    current_app.logger.exception(e)
    return CommonResult.failed(message=str(e))


# TODO 自定义接口，restful风格
@RequestMapping("/hello_world", [RequestMethod.POST])
@ResponseBody
def hello_world(param) -> CommonResult:
    """
    自定义接口\n
    :param param: 请求参数
    :return: 响应
    """
    result = base_service.run(param)
    return CommonResult.ok(data=result)


# TODO 自定义接口，文件处理相关
@RequestMapping("/upload", [RequestMethod.POST])
def upload(upload_file) -> Response:
    """
    上传文件\n
    :param upload_file: 上传的文件
    :return: 响应
    """
    result = TemporaryFile()
    result.write(upload_file.stream.read())
    result.seek(0)
    return send_file(result, mimetype=upload_file.mimetype, as_attachment=True, download_name=upload_file.filename, attachment_filename=upload_file.filename)
