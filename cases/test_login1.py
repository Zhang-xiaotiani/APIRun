"""
Project: APIRun
File: test_login
Created Date: 2025/2/9
Author: AILa
Email: zym822056523@gmail.com
Description: 
"""
import requests

# import jsonpath

"""
DS_022 登录-使用用户名能正确的登录用户
"""


def test_login():
    # TODO 1: 确定请求数据，发送请求
    public_data = {"application": "app", "application_client_type": "weixin"}
    data = {"accounts": "hami", "pwd": "123456", "type": "username"}
    res = requests.post(url="http://shop-xo.hctestedu.com/index.php?s=api/user/login",
                        params=public_data, json=data)
    # TODO 2: 获取响应数据进行断言,注意返回的是一个列表
    msg_results = res.json()['msg']
    # print(msg_results)
    # TODO 3: 进行断言处理
    assert msg_results == "登录成功"


if __name__ == "__main__":
    pass
