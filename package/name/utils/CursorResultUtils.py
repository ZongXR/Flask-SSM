# -*- coding: utf-8 -*-
from typing import List
from sqlalchemy.engine.cursor import CursorResult


def to_list(cursor_result: CursorResult) -> List[List]:
    """
    把SQL查询结果转化为二维列表以便进行json序列化\n
    :param cursor_result: 二维列表查询结果
    :return: 二位列表
    """
    return list(map(list, cursor_result))
