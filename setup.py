# -*- coding: utf-8 -*-
import setuptools


base_url = "https://github.com/GoogleLLP/Flask-SSM"
with open("./README.md", "r", encoding="utf-8") as f:
    long_description = f.read()
    long_description = long_description.replace("./test/demo", base_url + "/tree/main/test/demo")
    long_description = long_description.replace("./app.py", base_url + "/tree/main/app.py")
packages = list(filter(lambda x: not x.startswith("test"), setuptools.find_packages()))
requires_list = open('./requirements.txt', 'r', encoding='utf8').readlines()
requires_list = [x.strip() for x in requires_list if not x.startswith("PyMySQL")]


setuptools.setup(
    name="Flask-SSM",
    version="3.7.2.1",
    author="Xiangrui Zong",
    author_email="zxr@tju.edu.cn",
    description="A Flask based package imitate with Spring Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=base_url,
    packages=packages,
    license="GNU General Public License v3 (GPLv3)",
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
