# -*- coding: utf-8 -*-
import os


def recurse_files(path: str) -> [str]:
    """
    递归查询目录下所有文件\n
    :param path: 目录
    :return: 目录树
    """
    result = []
    if os.path.isfile(path):
        result.append(path)
    else:
        files = os.listdir(path)
        paths = map(lambda x: os.path.join(path, x), files)
        for path_one in paths:
            result.extend(recurse_files(path_one))
    return result


if __name__ == '__main__':
    files = recurse_files(r"C:\Users\DrZon\PycharmProjects\flask-mvc-example")
    for file in files:
        print(file)
