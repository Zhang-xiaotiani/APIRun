
'''
TODO 1: 确定请求数据，发送请求
TODO 2: 获取响应数据进行断言,注意返回的是一个列表
TODO 3: 进行断言处理
TODO 4: 获取token数据, 注意返回的是一个列表
'''
import allure

'''
通过添加对应的测试步骤：
- @allure.title("测试用例标题")
- with allure.step("接口步骤内容注释")

@allure.title("测试用例标题")
def test_case_name():
    with allure.step("第一步：XXXXX接口"):
        # 具体的接口请求代码
    with allure.step("第二步：XXXXX接口"):
        # 具体的接口请求代码
'''
import jsonpath
import pytest
import requests
token=''
@allure.title("登录测试")
def test_login001():
    global token
    with allure.step("登录的数据准备"):
        # TODO    1: 确定请求数据，发送请求
        url = "http://shop-xo.hctestedu.com/index.php?s=api/user/login"
        public_data = {"application": "app", "application_client_type": "weixin"}
        data = {"accounts": "hami", "pwd": "123456", "type": "username"}
    with allure.step("发送请求获得响应结果"):
        # TODO    2: 获取响应数据进行断言, 注意返回的是一个列表
        #1.发送请求   2.获取数据
        res=requests.post(url=url,params=public_data,data=data)
        msg_result=jsonpath.jsonpath(res.json(),'$.msg')[0]
    with allure.step("断言"):
        # TODO    3: 进行断言处理
        assert '登录成功' ==  msg_result
    with allure.step("获得登录成功之后的token"):
        # TODO    4: 获取token数据, 注意返回的是一个列表
        token=jsonpath.jsonpath(res.json(), '$..token')[0]

@allure.title("加入购物测试")
def test_addshopcar():
    # TODO    1: 确定请求数据，发送请求
    url = "http://shop-xo.hctestedu.com/index.php?s=/api/cart/save"
    public_data = {"application": "app", "application_client_type": "weixin", "token": token}
    data = {
        "goods_id": "11",
        "spec": [
            {
                "type": "尺寸",
                "value": "M"
            }
        ],
        "stock": "10"
    }
    # TODO    2: 获取响应数据进行断言, 注意返回的是一个列表
    res = requests.post(url=url, params=public_data, data=data)
    msg_result = jsonpath.jsonpath(res.json(), '$.msg')[0]
    assert '加入成功' == msg_result
    # TODO    3: 进行断言处理

# def test(expected=)
if __name__ == '__main__':
    pytest.main(['-vs',__file__])