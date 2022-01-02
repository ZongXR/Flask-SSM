# -*- coding: utf-8 -*-


def to_snake(old: str) -> str:
    """
    将字符串转为蛇形命名法\n
    :param old: 原始字符串
    :return: 新的字符串
    """
    if len(old) == 0:
        return old
    if len(old) == 1:
        return old.lower()
    result = old[1:]
    upper_letters = filter(lambda x: x.isupper(), result)
    for upper_letter in upper_letters:
        result = result.replace(upper_letter, "_" + upper_letter.lower())
    return old[0].lower() + result


if __name__ == '__main__':
    print(to_snake("FileService"))