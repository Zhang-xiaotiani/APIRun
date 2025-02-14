"""
Project: APIRun
File: test_add_car
Created Date: 2025/2/9
Author: AILa
Email: zym822056523@gmail.com
Description: 
"""
import allure

from core.globalContext import GlobalContext
from extend.KeyWords import KeyWords

api = KeyWords()
global_context = GlobalContext()

def test_add_car(get_token):
    token = get_token
    with allure.step("02 加入购物车"):
        # 案例二:加入购物车
        # TODO 1: 确定请求数据，发送请求
        url = "http://shop-xo.hctestedu.com/index.php?s=/api/cart/save"
        public_data = {"application": "app", "application_client_type": "weixin",
                       "token": token}
        # 第三种方式，全局私有变量
        #              "token": global_context.get("token")}
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
        # TODO 扩展 ：拼接数据进行传递
        request_data = {"method": "post", "url": url, "params": public_data, "data": data}
        res = api(**request_data)
        # print(res.text)
        # TODO 2: 获取响应数据进行断言,注意返回的是一个列表
        msg_results = res.json()["msg"]
        # TODO 3: 进行断言处理
        assert msg_results == "加入成功", f"断言失败,实际结果为{msg_results}"


if __name__ == "__main__":
    pass
