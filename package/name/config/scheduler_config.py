# -*- coding: utf-8 -*-
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from flask_apscheduler.auth import HTTPBasicAuth
from package.name.config.database_config import SQLALCHEMY_DATABASE_URI


SCHEDULER_JOBSTORES = {"default": SQLAlchemyJobStore(url=SQLALCHEMY_DATABASE_URI)}
SCHEDULER_TIMEZONE = 'Asia/Shanghai'
SCHEDULER_API_ENABLED = True
SCHEDULER_API_PREFIX = '/scheduler'
SCHEDULER_ALLOWED_HOSTS = ['*']
SCHEDULER_AUTH = None
SCHEDULER_EXECUTORS = {'default': {'type': 'threadpool', 'max_workers': 10}}
