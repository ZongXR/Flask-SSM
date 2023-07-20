# -*- coding: utf-8 -*-
from package.name.task import scheduler


# ID必须唯一
ID = "scheduled_task"
# 生效的函数名
FUNC = "my_func"
# 触发条件，interval表示定时间间隔触发
TRIGGER = "interval"
# 触发时间间隔设定5秒
SECONDS = 5
# 重启替换持久化
REPLACE_EXISTING = True


def my_func():
    """
    定时触发的函数\n
    :return: 空
    """
    scheduler.app.logger.info("触发定时任务" + ID)

