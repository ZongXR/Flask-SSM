#!/bin/bash
mkdir -p /opt/flask-mvc-example/logs
docker run -d -p 5000:5000 -v /opt/flask-mvc-example/logs:/opt/logs zongxr/flask-mvc-example:2.8.1.0