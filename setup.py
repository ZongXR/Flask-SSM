# -*- coding: utf-8 -*-
import setuptools


with open("./README.md", "r", encoding="utf-8") as f:
    long_description = f.read()
packages = list(filter(lambda x: not x.startswith("test"), setuptools.find_packages()))
requires_list = open('./requirements.txt', 'r', encoding='utf8').readlines()
requires_list = [x.strip() for x in requires_list]


setuptools.setup(
    name="Flask-SSM",
    version="3.4.0.0",
    author="Xiangrui Zong",
    author_email="zxr@tju.edu.cn",
    description="A Flask based package imitate with Spring Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GoogleLLP/Flask-SSM",
    packages=packages,
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries',
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    python_requires='>=3.7',
    install_requires=requires_list
)
