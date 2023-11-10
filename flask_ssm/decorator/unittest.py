# -*- coding: utf-8 -*-
import os
from flask import Flask
from flask_ssm.base.ssm import SpringApplication
from flask_ssm.utils.context_utils import has_app_context
from flask_ssm.utils.module_utils import get_package_from_path, find_member_from_multi_level_package
from flask_ssm.utils.time_utils import execute_time


class Test:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        if has_app_context():
            return self.func(*args, **kwargs)
        else:
            # change directory
            _path_tree_ = get_package_from_path(os.getcwd(), False, True)
            # find package name
            sps = find_member_from_multi_level_package(lambda x: isinstance(x, SpringApplication), _path_tree_)
            # build app context
            app = Flask(".".join(_path_tree_))
            for sp in sps:
                sp[1].init_app(app)
            # run original function
            with app.app_context():
                result, use_time = execute_time(self.func, *args, **kwargs)
                app.logger.info("执行用时: %dms" % use_time)
            return result
