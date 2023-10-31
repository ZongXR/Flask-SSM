# -*- coding: utf-8 -*-
import os
from types import FunctionType
from functools import wraps
from pathlib import Path
from flask import Flask
from flask.config import Config
from flask_apscheduler import APScheduler


scheduler = APScheduler()


def _add_app_context_(app: Flask, func: FunctionType) -> FunctionType:
    """
    对定时任务的执行函数加上下文\n
    :param app: flask的app
    :param func: 定时任务执行的函数
    :return: 加了上下文的定时任务的函数
    """
    @wraps(func)
    def result(*args, **kwargs):
        with app.app_context():
            return func(*args, **kwargs)
    return result


def init_scheduler(app: Flask):
    jobs = []
    cfg = Config(os.path.dirname(os.path.abspath(Path(__file__))))
    for _path_, _folders_, _files_ in os.walk(os.path.dirname(__file__), topdown=True):
        for _folder_ in _folders_:
            if _folder_.startswith("__"):
                _folders_.remove(_folder_)
        _package_name_ = __name__ + _path_.replace(os.path.dirname(__file__), "").replace(os.sep, ".")
        _files_ = list(filter(lambda x: not x.startswith("__"), _files_))
        _files_ = list(map(lambda x: x[0:-3], _files_))
        for _file_ in _files_:
            _module_ = __import__(_package_name_ + "." + _file_, fromlist=[_file_])
            cfg.clear()
            job = dict()
            cfg.from_object(_module_)
            for key, value in cfg.items():
                if key.isupper():
                    if "func" == key.lower():
                        job["func"] = __name__ + "." + _file_ + ":" + value
                        _task_function_ = getattr(_module_, value)
                        setattr(_module_, value, _add_app_context_(app, _task_function_))
                    else:
                        job[key.lower()] = value
            jobs.append(job)
    app.config.update({
        "SCHEDULER_API_ENABLED": True,
        "JOBS": jobs
    })
    scheduler.init_app(app)
    scheduler.start()
    app.logger.info("定时任务初始化成功")