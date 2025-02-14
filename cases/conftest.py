"""
Project: APIRun
File: conftest
Created Date: 2025/2/9
Author: AILa
Email: zym822056523@gmail.com
Description:  配置文件
"""
import logging
import time

import pytest
from jsonpath import jsonpath

from core.globalContext import GlobalContext
from extend.KeyWords import KeyWords
from extend.database.MysqlDriver import MysqlDriver

# from extend.APIRequest import APIRequest

api = KeyWords()
global_context = GlobalContext()
mysql = MysqlDriver()


@pytest.fixture(scope="module")
def get_token():
    # todo zym:  待改造为前置方法
    public_data = {"application": "app", "application_client_type": "weixin"}
    query_user = {

    }
    user_info = mysql.a_random_piece_of_data(**query_user)
    # res = requests.post(url="http://shop-xo.hctestedu.com/index.php?s=api/user/login",
    #                     params=public_data, json=data)
    request_data = {
        "method": "post",
        'url': "http://shop-xo.hctestedu.com/index.php?s=api/user/login",
        'params': public_data,
        'json': user_info
    }
    res = mysql.setup()
    # print(res.json())

    msg_results = res.json()['msg']
    assert msg_results == '登录成功', f'断言失败，实际结果为{msg_results}'

    token = jsonpath(res.json(), "$..token")[0]
    print(f"获取到的token值为：{token}")

    # 第三种方式，全局私有变量！
    # global_context.set_dict("token", token)
    return token


@pytest.fixture(scope="module")
def get_token_by_gcs():
    public_data = {"application": "app", "application_client_type": "weixin"}
    data = {"accounts": "ZYM001", "pwd": "123456", "type": "username"}
    # res = requests.post(url="http://shop-xo.hctestedu.com/index.php?s=api/user/login",
    #                     params=public_data, json=data)
    request_data = {
        "method": "post",
        'url': "http://shop-xo.hctestedu.com/index.php?s=api/user/login",
        'params': public_data,

        'json': data}
    res = api.send_HTTP_request(**request_data)
    # print(res.json())

    msg_results = res.json()['msg']
    assert msg_results == '登录成功', f'断言失败，实际结果为{msg_results}'

    token = jsonpath(res.json(), "$..token")[0]
    print(f"获取到的token值为：{token}")

    # 第三种方式，全局私有变量！
    global_context.set_dict("token", token)
    # return token


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    out = yield
    res = out.get_result()
    if res.when == "call":
        logging.info(f"用例ID：{res.nodeid}")
        logging.info(f"测试结果：{res.outcome}")
        logging.info(f"故障表示：{res.longrepr}")
        logging.info(f"异常：{call.excinfo}")
        logging.info(f"用例耗时：{res.duration}")
        logging.info("**************************************")


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    # 获取日志文件路径
    log_file_pattern = config.getini('log_file')
    if log_file_pattern:
        log_file = time.strftime(log_file_pattern)

        # 配置日志文件处理器
        file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')  # 'a' 表示追加模式
        file_handler.setLevel(logging.INFO)

        # 获取日志文件格式和日期格式
        log_file_format = config.getini('log_file_format')
        log_file_date_format = config.getini('log_file_date_format')
        formatter = logging.Formatter(log_file_format, log_file_date_format)
        file_handler.setFormatter(formatter)

        # 获取根日志记录器
        root_logger = logging.getLogger()
        root_logger.addHandler(file_handler)


if __name__ == "__main__":
    pass
