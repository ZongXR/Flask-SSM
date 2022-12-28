# -*- coding: utf-8 -*-
import os
from pathlib import Path
from flask import Flask
from flask.config import Config
from flask_apscheduler import APScheduler


def __recurse_files__(path: str) -> [str]:
    """
    递归查询目录下所有文件\n
    :param path: 目录
    :return: 目录树
    """
    result = []
    if os.path.isfile(path):
        result.append(path)
    else:
        files = os.listdir(path)
        paths = map(lambda x: os.path.join(path, x), files)
        for path_one in paths:
            if not os.path.dirname(path_one).split(os.path.sep)[-1].startswith("__"):
                result.extend(__recurse_files__(path_one))
    return result


_path_ = os.path.dirname(os.path.abspath(Path(__file__)))

scheduler = APScheduler()


def init_scheduler(app: Flask):
    jobs = []
    cfg = Config(_path_)
    for file in os.listdir(os.path.dirname(__file__)):
        if file.startswith("__"):
            continue
        full_file = os.path.join(os.path.dirname(__file__), file)
        if os.path.isfile(full_file):
            module_name = file[:-3]
            cfg.clear()
            job = dict()
            module = __import__(__name__ + "." + module_name, fromlist=[module_name])
            cfg.from_object(module)
            for key, value in cfg.items():
                if key.isupper():
                    if "func" == key.lower():
                        job["func"] = __name__ + "." + module_name + ":" + value
                    else:
                        job[key.lower()] = value
            jobs.append(job)
        else:
            files = __recurse_files__(full_file)
            for sub_file in files:
                module_name = os.path.basename(sub_file)
                path_name = os.path.dirname(sub_file)
                if module_name.startswith("__"):
                    continue
                package_name = __name__ + path_name.replace(os.path.dirname(__file__), "").replace(os.sep, ".")
                if "__" in package_name:
                    continue
                module_name = module_name[:-3]
                cfg.clear()
                job = dict()
                module = __import__(package_name + "." + module_name, fromlist=[module_name])
                cfg.from_object(module)
                for key, value in cfg.items():
                    if "func" == key.lower():
                        job["func"] = package_name + "." + module_name + ":" + value
                    else:
                        job[key.lower()] = value
                jobs.append(job)
    app.config.update({
        "SCHEDULER_API_ENABLED": True,
        "JOBS": jobs
    })
    scheduler.init_app(app)
    scheduler.start()
    app.logger.info("定时任务初始化成功并启动")