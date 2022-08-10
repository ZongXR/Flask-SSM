# -*- coding: utf-8 -*-
from logging.config import dictConfig
import os

path = os.getcwd()

dictConfig({
    "version": 1,
    "root": {"level": "DEBUG", "handlers": ["console", "debug", "info", "warn", "error"]},
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
            "filename": path + "/logs/DEBUG",
            "when": "MIDNIGHT",
            "backupCount": 1,
            "formatter": "default"
        },
        "info": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "INFO",
            "encoding": "utf-8",
            "filename": path + "/logs/INFO",
            "when": "MIDNIGHT",
            "backupCount": 1,
            "formatter": "default"
        },
        "warn": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "WARN",
            "encoding": "utf-8",
            "filename": path + "/logs/WARN",
            "when": "MIDNIGHT",
            "backupCount": 1,
            "formatter": "default"
        },
        "error": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "ERROR",
            "encoding": "utf-8",
            "filename": path + "/logs/ERROR",
            "when": "MIDNIGHT",
            "backupCount": 1,
            "formatter": "default"
        }
    }
})
