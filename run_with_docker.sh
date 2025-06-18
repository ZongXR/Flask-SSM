#!/bin/bash
mkdir -p /opt/flask-ssm-example/logs
docker run -d -p 5000:5000 -v /opt/flask-ssm-example/logs:/opt/logs zongxr/flask-ssm-example:3.9.2.1