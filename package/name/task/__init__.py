# -*- coding: utf-8 -*-
import os
import sys
from pathlib import Path
from flask import Flask
from flask.config import Config
from flask_apscheduler import APScheduler

_path_ = os.path.dirname(os.path.abspath(Path(__file__)))

scheduler = APScheduler()


def init_scheduler(app: Flask):
    jobs = []
    cfg = Config(_path_)
    for file in os.listdir(os.path.dirname(__file__)):
        module_name = file[:-3]
        if not module_name.startswith("__"):
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

    app.config.update({
        "SCHEDULER_API_ENABLED": True,
        "JOBS": jobs
    })
    scheduler.init_app(app)
    scheduler.start()
