"""
Project: APIRun
File: VarRender
Created Date: 2025/2/10
Author: AILa
Email: zym822056523@gmail.com
Description:  数据渲染
"""
from jinja2 import Template
import ast


def re_fresh(target, context):
    """
    :param target:  被替换的值
    :param context:  源字典
    :return:
    """
    return Template(str(target)).render(context)


if __name__ == "__main__":
    # target = {"name": "{{name}}", "age": "{{age}}"}
    # context = {"name": "jens", "age": "13"}
    # res = re_fresh(target, context)

    # print(res)
    # print(type(res))
    #
    # print("====================")
    # res = ast.literal_eval(res)
    # print(res)
    # print(type(res))
    pass