# -*- coding: utf-8 -*-
from flask_apscheduler.auth import HTTPBasicAuth


# TODO 定时任务相关配置，可自定义修改
SCHEDULER_JOBSTORES = None                # 定时任务存储位置，默认存储在内存中
SCHEDULER_TIMEZONE = 'Asia/Shanghai'      # 时区
SCHEDULER_API_ENABLED = True              # 是否开启修改定时任务的接口，默认开启
SCHEDULER_API_PREFIX = '/scheduler'       # 修改定时任务的接口前缀
SCHEDULER_ALLOWED_HOSTS = ['*']           # 允许修改定时任务的主机地址
SCHEDULER_AUTH = None                     # 修改定时任务接口认证，默认不开启
SCHEDULER_EXECUTORS = {'default': {'type': 'threadpool', 'max_workers': 10}}  # 定时任务线程池
