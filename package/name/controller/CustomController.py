# -*- coding: utf-8 -*-
from package.name.controller import bp
from flask import request, current_app, Response
from package.name.service import base_service
from package.name.vo import CommonResult
from package.name.exception import CustomException


@bp.errorhandler(CustomException)
def custom_error_handler(e: CustomException) -> Response:
    return CommonResult.failed(message=str(e), data=repr(e))


@bp.route("/custom", methods=["POST"])
def custom() -> Response:
    """
    自定义接口\n
    :return: 响应
    """
    param = request.json.get("question")
    result = base_service.run(int(param))
    return CommonResult.ok(data=result)
