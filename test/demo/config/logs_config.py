# -*- coding: utf-8 -*-
from logging.config import dictConfig
import os

__path__ = os.getcwd()


# TODO 日志相关配置，可自定义修改
dictConfig({
    "version": 1,
    # TODO 日志级别
    "root": {"level": "DEBUG", "handlers": ["console", "debug", "info", "warn", "error"]},
    # TODO 日志格式
    "formatters": {"default": {"format": "%(asctime)s - %(levelname)s - %(message)s"}},
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "stream": "ext://flask.logging.wsgi_errors_stream",
            "formatter": "default"
        },
        "debug": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "DEBUG",
            "encoding": "utf-8",
            # TODO 日志保存位置
            "filename": os.path.join(__path__, "logs/DEBUG"),
            "when": "MIDNIGHT",
            "backupCount": 1,
            "formatter": "default"
        },
        "info": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "INFO",
            "encoding": "utf-8",
            "filename": os.path.join(__path__, "logs/INFO"),
            "when": "MIDNIGHT",
            "backupCount": 1,
            "formatter": "default"
        },
        "warn": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "WARN",
            "encoding": "utf-8",
            "filename": os.path.join(__path__, "logs/WARN"),
            "when": "MIDNIGHT",
            "backupCount": 1,
            "formatter": "default"
        },
        "error": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "ERROR",
            "encoding": "utf-8",
            "filename": os.path.join(__path__, "logs/ERROR"),
            "when": "MIDNIGHT",
            "backupCount": 1,
            "formatter": "default"
        }
    }
})
