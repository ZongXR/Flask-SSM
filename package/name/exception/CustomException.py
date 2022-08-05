# -*- coding: utf-8 -*-


class CustomException(Exception):

    message: str

    def __init__(self, message: str, *args: object) -> None:
        """
        构造方法\n
        :param message: 消息
        :param args: 变长参数
        """
        super().__init__(*args)
        self.message = message

    def __str__(self) -> str:
        """
        格式化成字符串\n
        :return: 字符串
        """
        return self.message

    def __repr__(self) -> str:
        return type(self).__name__ + "('" + self.message + "')"

