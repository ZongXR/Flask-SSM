# -*- coding: utf-8 -*-
from package.name.controller import bp
from flask import request, current_app
from package.name.service import base_service


@bp.route("/custom", methods=["POST", "GET"])
def custom():
    """
    自定义接口\n
    :return: 响应
    """
    param = request.values.get("question")
    result = base_service.run(param)
    return result
