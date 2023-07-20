# -*- coding: utf-8 -*-


SCHEDULER_JOBSTORES = dict()
SCHEDULER_TIMEZONE = 'Asia/Shanghai'
SCHEDULER_API_ENABLED = True
SCHEDULER_API_PREFIX = '/scheduler'
SCHEDULER_ALLOWED_HOSTS = ['*']
SCHEDULER_AUTH = None
SCHEDULER_EXECUTORS = {'default': {'type': 'threadpool', 'max_workers': 10}}
