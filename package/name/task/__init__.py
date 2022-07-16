# -*- coding: utf-8 -*-
import os
import sys
from pathlib import Path
from flask import Flask
from flask.config import Config
from flask_apscheduler import APScheduler
from package.name.utils.DirUtils import recurse_files

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
            __import__(__name__ + "." + module_name)
            module = sys.modules[__name__ + "." + module_name]
            cfg.from_object(module)
            for key, value in cfg.items():
                if "func" == key.lower():
                    job["func"] = __name__ + "." + module_name + ":" + value
                else:
                    job[key.lower()] = value
            jobs.append(job)
        else:
            files = recurse_files(full_file)
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
                __import__(package_name + "." + module_name)
                module = sys.modules[package_name + "." + module_name]
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