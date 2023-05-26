# -*- coding: utf-8 -*-
import os


def test(func):
    """
    单元测试\n
    :param func: 需要测试的函数
    :return: 原函数的返回值
    """
    def wrapper(*args, **kwargs):
        # change directory
        path_idx = __file__[0:-3].rindex(__name__.replace(".", os.path.sep))
        os.chdir(__file__[0:path_idx])
        # build app context
        decorator_idx = __name__.rindex("decorator.unittest") - 1
        packages = __name__[0:decorator_idx]
        module = __import__(packages, fromlist=[packages.split(".")[-1]])
        app = module.create_app()
        # run original function
        with app.app_context():
            result = func(*args, **kwargs)
        return result
    return wrapper
