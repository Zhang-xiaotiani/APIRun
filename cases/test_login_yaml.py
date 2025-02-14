"""
Project: APIRun
File: test_login
Created Date: 2025/2/9
Author: AILa
Email: zym822056523@gmail.com
Description: 
"""
import allure
import pytest
import requests

from parse.YamlCaseParse import read_yaml

# import jsonpath
import os
print("工作目录",os.getcwd())
"""
DS_022 登录-使用用户名能正确的登录用户
"""
# {'datail': '正常登录', 'data': {'accounts': 'AA001', 'pwd': 123456, 'type': 'username'}, 'check': {'msg': '登录成功'}}
# filename = "D:\CodeLibrary\APIRun\cases\yaml_cases\yaml_login.yaml"
filename = "cases/yaml_cases/yaml_login.yaml"
# filename = "./yaml_cases/yaml_login.yaml"
data = read_yaml(file_name=filename)
# print(data)


@pytest.mark.parametrize("param", data)
@allure.title("登录测试")
def test_login(param):
    allure.dynamic.title("登录测试--" + param["datail"])

    public_data = {"application": "app", "application_client_type": "weixin"}
    data = param["data"]
    request_data = {'method': 'post',
                    'url': "http://shop-xo.hctestedu.com/index.php?s=api/user/login",
                    'params': public_data,
                    'json': data}
    res = requests.post(url="http://shop-xo.hctestedu.com/index.php?s=api/user/login",
                        params=public_data, json=data)

    msg_results = res.json()['msg']

    assert msg_results == param["check"]["msg"]
    print(res.json())


if __name__ == "__main__":
    pytest.main(['-vs'], __file__)
