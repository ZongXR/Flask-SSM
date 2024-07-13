# -*- coding: utf-8 -*-
from logging.config import dictConfig
import os


# TODO 日志保存位置
__path__ = os.path.join(os.getcwd(), "logs")
if not __path__:
    os.mkdir(__path__)


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
            "filename": os.path.join(__path__, "DEBUG"),
            "when": "MIDNIGHT",
            "backupCount": 1,
            "formatter": "default"
        },
        "info": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "INFO",
            "encoding": "utf-8",
            "filename": os.path.join(__path__, "INFO"),
            "when": "MIDNIGHT",
            "backupCount": 1,
            "formatter": "default"
        },
        "warn": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "WARN",
            "encoding": "utf-8",
            "filename": os.path.join(__path__, "WARN"),
            "when": "MIDNIGHT",
            "backupCount": 1,
            "formatter": "default"
        },
        "error": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "ERROR",
            "encoding": "utf-8",
            "filename": os.path.join(__path__, "ERROR"),
            "when": "MIDNIGHT",
            "backupCount": 1,
            "formatter": "default"
        }
    }
})
