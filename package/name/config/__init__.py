# -*- coding: utf-8 -*-
import os
from typing import List
from types import ModuleType
from flask import Flask


__modules__: List[ModuleType] = []
for _path_, _folders_, _files_ in os.walk(os.path.dirname(__file__), topdown=True):
    for _folder_ in _folders_:
        if _folder_.startswith("__"):
            _folders_.remove(_folder_)
    _package_name_ = __name__ + _path_.replace(os.path.dirname(__file__), "").replace(os.sep, ".")
    _files_ = list(filter(lambda x: not x.startswith("__"), _files_))
    _files_ = list(map(lambda x: x[0:-3], _files_))
    for _file_ in _files_:
        _module_ = __import__(_package_name_ + "." + _file_, fromlist=[_file_])
        __modules__.append(_module_)


def init_config(app: Flask):
    """
    初始化view层
    :param app:
    :return:
    """
    for __module__ in __modules__:
        app.config.from_object(__module__)
        for __key__ in dir(__module__):
            if __key__.isupper():
                __value__ = app.config.get(__key__)
                __env_value__ = os.getenv(__key__)
                if __env_value__ is not None:
                    if type(__value__) is str:
                        app.config[__key__] = __env_value__
                    else:
                        app.config[__key__] = eval(__env_value__)
    if app.config.get("EUREKA_ENABLED", None):
        eureka_client = __import__("py_eureka_client.eureka_client", fromlist=["eureka_client"])
        eureka_client.init(
            eureka_server=app.config.get("EUREKA_SERVICE_URL", "http://localhost:8761/eureka/"),
            app_name=app.config.get("EUREKA_SERVICE_NAME", app.name),
            # 当前组件的主机名，可选参数，如果不填写会自动计算一个，如果服务和 eureka 服务器部署在同一台机器，请必须填写，否则会计算出 127.0.0.1
            instance_host=app.config.get("EUREKA_INSTANCE_HOSTNAME", "localhost"),
            instance_port=app.config.get("APP_PORT", 5000),
            renewal_interval_in_secs=app.config.get("EUREKA_HEARTBEAT", 90),
            # 调用其他服务时的高可用策略，可选，默认为随机
            ha_strategy=eureka_client.HA_STRATEGY_RANDOM
        )
    app.logger.info("初始化配置成功")
