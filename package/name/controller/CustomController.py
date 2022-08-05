# -*- coding: utf-8 -*-
from package.name.controller import bp
from flask import request, current_app, Response
from package.name.service import base_service
from package.name.vo.CommonResult import CommonResult


@bp.route("/custom", methods=["POST"])
def custom() -> Response:
    """
    自定义接口\n
    :return: 响应
    """
    param = request.json.get("question")
    result = base_service.run(int(param))
    return CommonResult.ok(data=result)
