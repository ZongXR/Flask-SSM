# -*- coding: utf-8 -*-
from json import dumps
from flask import jsonify, Response


class CommonResult(object):

    code: int

    message: str

    data: object

    def __init__(self, code: int, message: str, data: object) -> None:
        """
        构造方法\n
        :param code: 状态码
        :param message: 消息
        :param data: 响应正文
        """
        super().__init__()
        self.code = code
        self.message = message
        self.data = data

    @staticmethod
    def ok(message: str = "OK", data: object = None) -> Response:
        """
        请求成功\n
        :param message: 消息
        :param data: 响应正文
        :return: 响应
        """
        result = CommonResult(code=200, message=message, data=data)
        return jsonify(result.__dict__)

    @staticmethod
    def bad_request(message: str = "Bad Request", data: object = None) -> Response:
        """
        请求坏了\n
        :param message: 消息
        :param data: 响应正文
        :return: 响应
        """
        result = CommonResult(code=400, message=message, data=data)
        return jsonify(result.__dict__)

    @staticmethod
    def not_found(message: str = "Not Found", data: object = None) -> Response:
        """
        没找到\n
        :param message: 消息
        :param data: 响应正文
        :return: 响应
        """
        result = CommonResult(code=404, message=message, data=data)
        return jsonify(result.__dict__)

    @staticmethod
    def failed(message: str = "Internal Server Error", data: object = None) -> Response:
        """
        请求失败\n
        :param message: 消息
        :param data: 响应正文
        :return: 响应
        """
        result = CommonResult(code=500, message=message, data=data)
        return jsonify(result.__dict__)

    @staticmethod
    def make_response(code: int, message: str, data: object) -> Response:
        """
        制作一个响应\n
        :param code: 状态码
        :param message: 消息
        :param data: 响应正文
        :return: 响应
        """
        result = CommonResult(code=code, message=message, data=data)
        return jsonify(result.__dict__)

    def __str__(self) -> str:
        return dumps(self.__dict__)


if __name__ == '__main__':
    print(CommonResult.failed("ll"))
