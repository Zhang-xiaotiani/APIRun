"""
Project: APIRun
File: convert_string_to_dict
Created Date: 2025/2/10
Author: AILa
Email: zym822056523@gmail.com
Description:  字符串转字典，暂时无用
"""
import ast


def convert_string_to_dict(data):
    # 判断是否是字典类型
    if isinstance(data, dict):
        for key, value in data.items():
            # 如果值是字符串并且符合字典格式，尝试转换
            if isinstance(value, str):
                try:
                    # 尝试将字符串转换为字典
                    data[key] = ast.literal_eval(value)
                except (ValueError, SyntaxError):
                    # 如果转换失败，则保留原始值
                    continue
            # 如果值是字典，递归处理
            elif isinstance(value, dict):
                convert_string_to_dict(value)
    return data


if __name__ == "__main__":
    pass
