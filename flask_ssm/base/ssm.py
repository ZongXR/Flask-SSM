# -*- coding: utf-8 -*-
import os
from typing import List, Optional
from types import ModuleType
import inspect
import pkgutil
import logging
from pathlib import Path
from functools import wraps
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from flask import Flask, Blueprint
from flask.config import Config
from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_ssm.utils.module_utils import walk_sub_modules
from flask_ssm.utils.context_utils import add_app_context
from flask_ssm.utils.type_utils import pojo_private_properties


class Controller:
    """
    接口\n
    """
    pass


class Service:
    """
    业务逻辑\n
    """
    pass


class Repository:
    """
    数据交互\n
    """
    db = SQLAlchemy()


class Configuration:
    """
    配置项\n
    """
    pass


class Scheduled:
    """
    定时任务\n
    """
    pass


class Bean:
    pass


class SpringApplication:

    def __init__(self):
        """
        构造方法\n
        """
        self.orm: Optional[SQLAlchemy] = None
        self.scheduler = APScheduler()
        # 记录下哪些包需要自动导入
        self.__config_packages__: List[ModuleType] = list()
        self.__controller_packages__: List[ModuleType] = list()
        self.__service_packages__: List[ModuleType] = list()
        self.__dao_packages__: List[ModuleType] = list()
        self.__task_packages__: List[ModuleType] = list()
        self.__pojo_packages__: List[ModuleType] = list()
        # 遍历子包，自动导入
        self.base_package = inspect.getmodule(inspect.stack()[1].frame)
        for _sub_package_ in pkgutil.iter_modules([os.path.dirname(self.base_package.__file__)]):
            if _sub_package_.ispkg:
                _import_package_ = __import__(".".join([self.base_package.__package__, _sub_package_.name]), fromlist=[_sub_package_.name])
                if inspect.getmembers(_import_package_, lambda x: x is Configuration):
                    self.__config_packages__.append(_import_package_)
                    logging.info("已发现config包: " + _import_package_.__package__)
                if inspect.getmembers(_import_package_, lambda x: x is Controller):
                    self.__controller_packages__.append(_import_package_)
                    logging.info("已发现controller包: " + _import_package_.__package__)
                if inspect.getmembers(_import_package_, lambda x: x is Repository):
                    self.__dao_packages__.append(_import_package_)
                    for cls_name, cls in inspect.getmembers(_import_package_, lambda x: x is Repository):
                        for var_name, var in inspect.getmembers(cls, lambda x: isinstance(x, SQLAlchemy)):
                            if self.orm is None:
                                self.orm = var
                            else:
                                setattr(cls, var_name, self.orm)
                    logging.info("已发现dao包: " + _import_package_.__package__)
                if inspect.getmembers(_import_package_, lambda x: x is Service):
                    self.__service_packages__.append(_import_package_)
                    logging.info("已发现service包： " + _import_package_.__package__)
                if inspect.getmembers(_import_package_, lambda x: x is Scheduled):
                    self.__task_packages__.append(_import_package_)
                    logging.info("已发现task包: " + _import_package_.__package__)
                if inspect.getmembers(_import_package_, lambda x: x is Bean):
                    self.__pojo_packages__.append(_import_package_)
                    logging.info("已发现pojo包: " + _import_package_.__package__)

    def init_app(self, app: Flask):
        """
        初始化框架\n
        :param app: Flask对象
        :return:
        """
        self.__init_config__(app)
        # self.__init_pojo__(app)
        self.__init_dao__(app)
        self.__init_service__(app)
        self.__init_controller__(app)
        self.__init_task__(app)
        self.__init_cors__(app)
        self.__init_run__(app)

    def __init_config__(self, app: Flask):
        """
        初始化配置包\n
        :param app: Flask对象
        :return:
        """
        for __config_package__ in self.__config_packages__:
            for __config_module__ in walk_sub_modules(__config_package__):
                app.config.from_object(__config_module__)
                for __key__ in dir(__config_module__):
                    if __key__.isupper():
                        __value__ = app.config.get(__key__)
                        __env_value__ = os.getenv(__key__)
                        if __env_value__ is not None:
                            if type(__value__) is str:
                                app.config[__key__] = __env_value__
                            else:
                                app.config[__key__] = eval(__env_value__)
        app.logger.info("初始化配置成功")

    def __init_controller__(self, app: Flask):
        """
        初始化controller\n
        :param app: Flask对象
        :return:
        """
        for __controller_package__ in self.__controller_packages__:
            for __controller_module__ in walk_sub_modules(__controller_package__):
                _blueprints_ = inspect.getmembers(__controller_module__, lambda x: isinstance(x, Blueprint))
                for _blueprint_ in _blueprints_:
                    app.register_blueprint(_blueprint_[1])
        app.logger.info("初始化视图成功")

    def __init_dao__(self, app: Flask):
        """
        初始化数据交互层\n
        :param app: Flask对象
        :return:
        """
        self.orm.init_app(app)
        for __dao_package__ in self.__dao_packages__:
            for __dao_module__ in walk_sub_modules(__dao_package__):
                setattr(__dao_module__, "__orm__", self.orm)
        app.logger.info("初始化数据库连接成功")

    def __init_task__(self, app: Flask):
        """
        初始化定时任务\n
        :param app: Flask对象
        :return:
        """
        jobs = list()
        for __task_package__ in self.__task_packages__:
            cfg = Config(os.path.dirname(os.path.abspath(Path(__task_package__.__file__))))
            for __task_module__ in walk_sub_modules(__task_package__):
                setattr(__task_module__, "__orm__", self.orm)
                cfg.clear()
                job = dict()
                cfg.from_object(__task_module__)
                for key, value in cfg.items():
                    if key.isupper():
                        if "func" == key.lower():
                            job["func"] = __task_module__.__name__ + ":" + value
                            _task_function_ = getattr(__task_module__, value)
                            setattr(__task_module__, value, add_app_context(app, _task_function_))
                        else:
                            job[key.lower()] = value
                jobs.append(job)
        app.config.update({
            "JOBS": jobs
        })
        self.scheduler.init_app(app)
        self.scheduler.start()
        app.logger.info("初始化定时任务成功")

    def __init_service__(self, app: Flask):
        """
        初始化service包\n
        :param app: Flask对象
        :return:
        """
        for __service_package__ in self.__service_packages__:
            for __service_module__ in walk_sub_modules(__service_package__):
                setattr(__service_module__, "__orm__", self.orm)
        app.logger.info("初始化业务逻辑成功")

    def __init_pojo__(self, app: Flask):
        """
        初始化pojo包\n
        :param app: Flask对象
        :return:
        """
        for __pojo_package__ in self.__pojo_packages__:
            for __pojo_module__ in walk_sub_modules(__pojo_package__):
                members = inspect.getmembers(__pojo_module__)
                members = filter(lambda x: inspect.isclass(x[1]) and x[1].__module__ == __pojo_module__.__name__, members)
                for name, cls in members:
                    if not issubclass(cls, self.orm.Model):
                        metadata = pojo_private_properties(cls)
                        cls = type(cls.__name__, (self.orm.Model, cls), metadata)
                        setattr(__pojo_module__, name, cls)
        app.logger.info("初始化映射对象成功")

    def __init_cors__(self, app: Flask):
        """
        初始化跨域\n
        :param app:
        :return:
        """
        CORS(app, supports_credentials=True)
        app.logger.info("初始化跨域成功")

    def __init_run__(self, app: Flask):
        """
        修改app的run函数\n
        :param app: Flask对象
        :return:
        """
        @wraps(app.run)
        def run(*args, **kwargs):
            kwargs["host"] = kwargs.get("host", app.config.get("APP_HOST", None))
            kwargs["port"] = kwargs.get("port", app.config.get("APP_PORT", None))
            kwargs["threaded"] = kwargs.get("threaded", app.config.get("APP_THREAD", None))
            kwargs["processes"] = kwargs.get("processes", app.config.get("APP_PROCESS", None))
            kwargs["use_reloader"] = kwargs.get("use_reloader", app.config.get("USE_RELOADER", None))
            param_names = list(inspect.signature(app.run).parameters.keys())
            for i, arg in enumerate(args):
                kwargs[param_names[i]] = arg
            return Flask.run(app, **kwargs)
        mounts = None if app.config.get("APPLICATION_ROOT", "/") == "/" else {app.config.get("APPLICATION_ROOT", "/"): app}
        app.wsgi_app = DispatcherMiddleware(app.wsgi_app, mounts=mounts)
        app.run = run
        app.logger.info("初始化运行入口成功")
