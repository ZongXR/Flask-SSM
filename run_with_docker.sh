#!/bin/bash
docker run -d -p 5000:5000 -v /opt/flask-ssm-example/logs:/opt/logs zongxr/flask-ssm-example:3.10.8.1