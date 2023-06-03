# -*- coding: utf-8 -*-
import os
import flask.globals as globs


def test(func):
    """
    单元测试\n
    :param func: 需要测试的函数
    :return: 原函数的返回值
    """
    def wrapper(*args, **kwargs):
        _app_ctx_stack = getattr(globs, "_app_ctx_stack", None)
        if _app_ctx_stack.top is None:
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
        else:
            return func(*args, **kwargs)
    return wrapper
