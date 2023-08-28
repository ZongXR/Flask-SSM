# -*- coding: utf-8 -*-
import socket


# TODO eureka 注册机制相关，可自定义修改
EUREKA_ENABLED = False                                # 是否开启eureka客户端
EUREKA_SERVICE_NAME = "flask-mvc-example"             # 在eureka注册中心显示的名称
EUREKA_SERVICE_URL = "http://localhost:8761/eureka/"  # eureka注册中心地址
EUREKA_INSTANCE_HOSTNAME = socket.gethostname()       # 应用的host
EUREKA_HOME_PAGE_URL = "https://github.com/GoogleLLP/flask-mvc-example"   # 介绍该应用的URL
EUREKA_HEARTBEAT = 90                                 # 联络eureka的心跳包，单位秒
