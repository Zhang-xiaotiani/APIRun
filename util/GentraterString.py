"""
Project: APIRun
File: GentraterString
Created Date: 2025/2/11
Author: AILa
Email: zym822056523@gmail.com
Description: 
"""
import string

import random


# 随机生成default_prefix为前缀+6长度的字符串，所选集合为：
#                             0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
def generator_string(default_prefix: str = "") -> str:
    res = default_prefix + "_" + "".join(random.choice(string.printable[:-38]) for _ in range(6))
    # print("generator_string====================",res)
    return res


if __name__ == "__main__":
    print(generator_string("ZYM"))
