# -*- coding: utf-8 -*-
import socket


EUREKA_ENABLED = False
SERVICE_NAME = "flask-mvc-example"
EUREKA_SERVICE_URL = "http://localhost:8761/eureka/"
EUREKA_INSTANCE_HOSTNAME = socket.gethostname()
EUREKA_HOME_PAGE_URL = "https://github.com/GoogleLLP/flask-mvc-example"
EUREKA_HEARTBEAT = 90
