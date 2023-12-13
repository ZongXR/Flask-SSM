FROM python:3.7.3
MAINTAINER ZongXiangrui<zxr@tju.edu.cn>
WORKDIR /opt
# 准备环境
COPY . /opt
VOLUME ["/opt/logs"]
EXPOSE 5000
RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple -r /opt/requirements.txt
RUN pip3 install Flask-SSM==3.7.1.2
# 启动
CMD python3 ./app.py
