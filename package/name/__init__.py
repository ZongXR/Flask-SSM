# -*- coding: utf-8 -*-
import os
from flask import Flask
from flask_cors import CORS


def create_app() -> Flask:
    """
    创建应用\n
    :return:
    """
    app = Flask(__name__)
    if "config" in os.listdir(os.path.dirname(__file__)):
        logs_config = __import__(".".join([__name__, "config", "logs_config"]), fromlist=["logs_config"])
        database_config = __import__(".".join([__name__, "config", "database_config"]), fromlist=["database_config"])
        app.config.from_object(database_config)
    if "dao" in os.listdir(os.path.dirname(__file__)):
        dao = __import__(".".join([__name__, "dao"]), fromlist=["dao"])
        if "init_db" in dir(dao):
            dao.init_db(app)
    if "controller" in os.listdir(os.path.dirname(__file__)):
        controller = __import__(".".join([__name__, "controller"]), fromlist=["controller"])
        if "init_view" in dir(controller):
            controller.init_view(app)
    if "task" in os.listdir(os.path.dirname(__file__)):
        task = __import__(".".join([__name__, "task"]), fromlist=["task"])
        if "init_scheduler" in dir(task):
            task.init_scheduler(app)
    CORS(app, supports_credentials=True)
    app.logger.info("web应用启动成功")
    return app
