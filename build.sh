#!/bin/bash
docker build -t zongxr/flask-ssm-example:3.9.0.0 .
python3 setup.py sdist bdist_wheel
python3 -m twine upload --repository testpypi dist/*
python3 -m twine upload dist/*