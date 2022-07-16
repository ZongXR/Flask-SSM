# -*- coding: utf-8 -*-
from flask import Flask
from flask_cors import CORS
from package.name.config import DatabaseConfig, LogsConfig
from package.name.dao import init_db
from package.name.controller import init_view
from package.name.task import init_scheduler


def create_app() -> Flask:
    """
    创建应用\n
    :return:
    """
    app = Flask(__name__)
    app.config.from_object(DatabaseConfig)
    init_db(app)
    init_view(app)
    init_scheduler(app)
    CORS(app, supports_credentials=True)
    app.logger.info("web应用启动成功")
    return app
