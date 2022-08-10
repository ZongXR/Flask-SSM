# -*- coding: utf-8 -*-
import os
from flask import request, current_app, Response, Blueprint
from package.name.service import base_service
from package.name.vo import CommonResult
from package.name.exception import CustomException


# 自动注册蓝图，此行代码不要动
bp = Blueprint(__name__.replace(".", "_"), __name__, static_folder=os.path.join(os.getcwd(), "static"), template_folder=os.path.join(os.getcwd(), "templates"), static_url_path="")


# TODO 在这里写自己的异常处理handler
@bp.errorhandler(CustomException)
def custom_error_handler(e: CustomException) -> Response:
    current_app.logger.exception(e)
    return CommonResult.failed(message=str(e), data=repr(e))


# TODO 从这以下写自己的接口
@bp.route("/custom", methods=["POST"])
def custom() -> Response:
    """
    自定义接口\n
    :return: 响应
    """
    param = request.json.get("question")
    result = base_service.run(param)
    return CommonResult.ok(data=result)
