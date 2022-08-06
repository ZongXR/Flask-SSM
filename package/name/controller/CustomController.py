# -*- coding: utf-8 -*-
from flask import request, current_app, Response
from package.name.controller import bp_custom
from package.name.service import base_service
from package.name.vo import CommonResult
from package.name.exception import CustomException


@bp_custom.errorhandler(CustomException)
def custom_error_handler(e: CustomException) -> Response:
    return CommonResult.failed(message=str(e), data=repr(e))


@bp_custom.route("/custom", methods=["POST"])
def custom() -> Response:
    """
    自定义接口\n
    :return: 响应
    """
    param = request.json.get("question")
    result = base_service.run(int(param))
    return CommonResult.ok(data=result)
