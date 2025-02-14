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

from parse.EXCELCaseParse import read_excel
from parse.YamlCaseParse import read_yaml

# import jsonpath

"""
DS_022 登录-使用用户名能正确的登录用户
"""
# {'datail': '正常登录', 'data': {'accounts': 'AA001', 'pwd': 123456, 'type': 'username'}, 'check': {'msg': '登录成功'}}
filename = r"D:\CodeLibrary\APIRun\cases\excel_cases\testcaselogin.xlsx"
data = read_excel(file_name=filename)

print(data)


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

    # print("登录测试--" + param["datail"] + str(res.text))
    assert msg_results == param["check"]["msg"]


if __name__ == "__main__":
    pytest.main(['-vs'], __file__)
