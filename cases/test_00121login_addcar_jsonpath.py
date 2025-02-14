
'''
1.提取响应数据并存储到全局变量--extend/keyworks.py
2.数据的渲染（数据值的替换）--utils/VarRender.py
3.自定义函数的应用
4.日志功能实现及应用--pytest.ini  and conftest.py
'''
import allure
import jsonpath
import pytest
from extend.KeyWords import KeyWords

token=''
keyword=KeyWords()
@allure.title("登录测试002")
def test_login002():

    with allure.step("登录的数据准备"):
        # TODO    1: 确定请求数据，发送请求
        url = "http://shop-xo.hctestedu.com/index.php?s=api/user/login"
        public_data = {"application": "app", "application_client_type": "weixin"}
        data = {"accounts": "hami", "pwd": "123456", "type": "username"}
    with allure.step("发送请求获得响应结果"):
        # TODO    2: 获取响应数据进行断言, 注意返回的是一个列表
        #1.发送请求   2.获取数据
        #组装
        senddata = {'url':url,'params':public_data,'data':data}
        res=keyword.send_HTTP_request(**senddata)
        #msg_result=jsonpath.jsonpath(res.json(),'$.msg')[0]
        msg_result = keyword.extend_json_data_by_jsonpath(EXVALUE="$.msg",INDEX=0,VARNAME='msg_result')
    with allure.step("断言"):
        # TODO    3: 进行断言处理
        assert '登录成功' ==  msg_result


@allure.title("加入购物测试")
def test_addshopcar001(get_token):
    token=get_token
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
    # 组装
    senddata = {'url': url, 'params': public_data, 'data': data}
    res = keyword.send_HTTP_request(**senddata)
    msg_result = keyword.extend_json_data_by_jsonpath(EXVALUE="$.msg", INDEX=0, VARNAME='msg_result')
    assert '加入成功' == msg_result
    # TODO    3: 进行断言处理


if __name__ == '__main__':
    pytest.main(['-vs',__file__])
