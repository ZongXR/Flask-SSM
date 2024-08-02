#!/bin/bash
docker build -t zongxr/flask-ssm-example:3.8.0.1 .
python3 setup.py sdist bdist_wheel
python3 -m twine upload --repository testpypi dist/*
python3 -m twine upload dist/*