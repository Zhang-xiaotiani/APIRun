"""
Project: APIRun
File: globalContext
Created Date: 2025/2/9
Author: AILa
Email: zym822056523@gmail.com
Description:  全局私有变量封装
"""
from enum import Enum


class GlobalContext(object):
    _dict = {}  # 变量以_开头为内置属性，外部不可修改，即使实例不同

    # 常量
    CURRENT_RESPONSE = "current_response"

    # 字典中加  键值对
    def set_dict(self, key, value):
        self._dict[key] = value

    #
    def set_by_dict(self, dic):
        self._dict.update(dic)

    # 获取val
    def get_value(self, key):
        return self._dict.get(key, None)

    # 获得字典
    def get_all_value(self):
        return self._dict


if __name__ == "__main__":
    pass
