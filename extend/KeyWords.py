"""
Project: APIRun
File: APIRequest
Created Date: 2025/2/9
Author: AILa
Email: zym822056523@gmail.com
Description: 
"""
import json
import logging
from datetime import datetime

import allure
import requests

from jsonpath import jsonpath

from core.globalContext import GlobalContext
from parse.YamlCaseParse import read_yaml
from util.dict_lowwer import dict_lowwer

global_context = GlobalContext()


class KeyWords:
    def __init__(self):
        self.session = requests.session()
        self._supported_methods = {'get', 'post', 'put', 'delete', 'GET', 'POST', 'PUT', 'DELETE'}

    @allure.step("发送HTTP请求")
    def send_HTTP_request(self, **kwargs):
        """
        发送 HTTP 请求。

        :param url: 请求的URL地址
        :param method: 请求方法，支持'GET'、'POST'、'PUT'、'DELETE'
        :param param_type: 参数类型，可以是 'form' 或 'json'（默认为 'json'）
        :param data: 请求体中的数据
        :param kwargs: 额外的请求参数，如headers、params等
        :return: 返回requests.Response对象，包含HTTP响应
        :raises ValueError: 如果提供了不支持的请求方法，抛出异常
        """
        kwargs = dict_lowwer(kwargs)

        method = kwargs.get("method", "post")
        if method:
            method = method.upper()
        param_type = kwargs.get("param_type", None)

        if method not in self._supported_methods:
            raise ValueError(f"不支持的请求方法:{method}")

        param_field = "params" if method == "GET" else ("form" if param_type == "form" else "json")
        params = kwargs.get("params", None)
        headers = kwargs.get("headers", None)
        url = kwargs.get("url", None)
        data = kwargs.get("data", None)
        # print(url, "====url")
        request_args = {
            "method": method,
            "url": url,
            param_field: data,
            "params": params,
            "headers": headers,
            # **kwargs
        }
        # res = self.session.request(**request_args)
        res = requests.request(**request_args)
        global_context.set_dict(GlobalContext.CURRENT_RESPONSE, res)
        print(res.text)
        logging.info("zymtest============" + res.text)

        return res

    def __call__(self, *args, **kwargs):
        """
        重载__call__方法，直接使用对象调用时调用send_HTTP_request方法。

        :param args: 位置参数
        :param kwargs: 关键字参数
        :return: 返回send_HTTP_request方法的结果
        """
        return self.send_HTTP_request(**kwargs)

    def close_session(self):
        self.session.close()

    @allure.step("使用jsonpath从响应数据中提取值并存入全局上下文。")
    def extend_json_data_by_jsonpath(self, EXVALUE=None, INDEX=0, VARNAME="", **kwargs):
        """
        使用jsonpath从响应数据中提取值并存入全局上下文。

        :param EXVALUE: 需要提取的json路径
        :param INDEX: 提取值的索引（用于处理返回数组）
        :param VARNAME: 提取的结果存储在全局上下文中的变量名
        :param kwargs: 其他额外参数
        :return: 返回提取的结果
        """
        #         获取response中对应的结果
        kwargs = dict_lowwer(kwargs)
        path = kwargs.get("exvalue", EXVALUE)
        index = kwargs.get('index', INDEX)
        VARNAME = kwargs.get("varname", VARNAME)

        response = global_context.get_value(GlobalContext.CURRENT_RESPONSE)
        ex_data = jsonpath(response.json(), path)[index]

        global_context.set_dict(VARNAME, ex_data)
        return ex_data

    @allure.step("数据加密")
    def sign_encryption(self, **kwargs):
        from extend.encryption.SignEncryption import Encryption
        return Encryption().sign_encryption(**kwargs)

    @allure.step("提取MySQL数据库中的数据并存储")
    def ex_mysqlData(self, **kwargs):
        from extend.database.MysqlDriver import MysqlDriver
        return MysqlDriver().ex_mysqlData(**kwargs)

    @staticmethod
    @allure.step("断言当前文本")
    def assert_text_comparators(**kwargs):
        from extend.Assert.AssertFunc import AssertComparators
        return AssertComparators().assert_text_comparators(**kwargs)

    @staticmethod
    @allure.step("断言当前json文本")
    def assert_json_comparators(**kwargs):
        from extend.Assert.AssertFunc import AssertComparators
        return AssertComparators().assert_json_comparators(**kwargs)

    @allure.step("全量断言")
    def assert_json_DeepDiff(self, **kwargs):
        from extend.Assert.DeepDiff import AssertDeepDiff
        return AssertDeepDiff().assert_json_DeepDiff(**kwargs)

    @allure.step("参数数据：发送Post请求-form_data--文件上传的请求")
    def request_post_form_urlencoded(self, **kwargs):
        """
        发送Post请求
        """
        url = kwargs.get("URL", None)
        files = kwargs.get("FILES", None)
        params = kwargs.get("PARAMS", None)
        headers = kwargs.get("HEADERS", None)
        data = kwargs.get("DATA", None)

        request_data = {
            "url": url,
            "params": params,
            "headers": headers,
            "data": data,
            "files": eval(files)  # 变成字典格式
        }

        response = requests.post(**request_data)
        print("response", response.json())
        global_context.set_dict("current_response", response)  # 默认设置成全局变量
        print("-----------------------")
        print(response.json())
        print("-----------------------")
        return response
#
# if __name__ == '__main__':
#     httprequests = APIRequest()
#     url = 'http://shop-xo.hctestedu.com?s=api/user/login'
#     params = {'application': 'app',
#               'application_client_type': 'weixin'}
#     data = {"accounts": "AA001",
#             "pwd": "123456",
#             "type": "username"}
#     request_data = {"method": "post",
#                     "url": url,
#                     "data": data,
#                     "params": params}
#     # res = requests.request(**request_data)
#     r = httprequests.send_HTTP_request(**request_data)
#     print(r.text)
#     httprequests.close_session()
