"""
Project: APIRun
File: dict_lowwer
Created Date: 2025/2/10
Author: AILa
Email: zym822056523@gmail.com
Description: 
"""


def dict_lowwer(d: dict) -> dict:
    res = {key.lower(): value for key, value in d.items()}
    return res


if __name__ == "__main__":
    pass
