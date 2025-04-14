# -*- coding: utf-8 -*-
from json import dumps
from pydantic import BaseModel, ConfigDict, Field


class CommonResult(BaseModel):

    model_config = ConfigDict(arbitrary_types_allowed=True)

    code: int = Field(default=200, description="status code")

    message: str = Field(default="OK", description="response message")

    data: object = Field(default=None, description="response data")

    def __init__(self, code: int, message: str, data: object):
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
    def ok(message: str = "OK", data: object = None):
        """
        请求成功\n
        :param message: 消息
        :param data: 响应正文
        :return: 响应
        """
        result = CommonResult(code=200, message=message, data=data)
        return result

    @staticmethod
    def bad_request(message: str = "Bad Request", data: object = None):
        """
        请求坏了\n
        :param message: 消息
        :param data: 响应正文
        :return: 响应
        """
        result = CommonResult(code=400, message=message, data=data)
        return result

    @staticmethod
    def not_found(message: str = "Not Found", data: object = None):
        """
        没找到\n
        :param message: 消息
        :param data: 响应正文
        :return: 响应
        """
        result = CommonResult(code=404, message=message, data=data)
        return result

    @staticmethod
    def failed(message: str = "Internal Server Error", data: object = None):
        """
        请求失败\n
        :param message: 消息
        :param data: 响应正文
        :return: 响应
        """
        result = CommonResult(code=500, message=message, data=data)
        return result

    @staticmethod
    def make_response(code: int, message: str, data: object):
        """
        制作一个响应\n
        :param code: 状态码
        :param message: 消息
        :param data: 响应正文
        :return: 响应
        """
        result = CommonResult(code=code, message=message, data=data)
        return result

    def __str__(self) -> str:
        return dumps(self.__dict__)


if __name__ == '__main__':
    print(CommonResult.failed("ll"))
