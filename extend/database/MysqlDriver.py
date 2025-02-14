"""
Project: APIRun
File: MysqlDriver
Created Date: 2025/2/11
Author: AILa
Email: zym822056523@gmail.com
Description: 
"""
import base64

import allure
import pymysql
from jsonpath import jsonpath
from pymysql import cursors

from core.globalContext import GlobalContext
from extend.KeyWords import KeyWords
from parse.YamlCaseParse import read_yaml
from util.CaseInfo import CaseInfo

keywords = KeyWords()
gc = GlobalContext()
# user_info : {'id': 30927, 'username': 'ZYM_gsbWRX', 'pwd': '4077a596c0147bb2559df2c42b69c1ab', 'gender': 0}
user_info = {}
token = ''


class MysqlDriver:
    DB_CONFIG = "db_conf"
    QUERY_CONTENT = "query_content"
    QUERY_TABLE = "table"
    QUERY_CONDITION_WHERE = "query_condition_where"
    QUERY_CONDITION_GROUP = "query_condition_group"
    QUERY_CONDITION_HAVING = "query_condition_having"
    QUERY_CONDITION_ORDER = "query_condition_order"
    QUERY_CONDITION_LIMIT = "query_condition_limit"

    @allure.step("获取sx_user表中的username,pwd,usertype进行前置登录获取必要的token等")
    def setup(self, **kwargs):

        global token
        self.a_random_piece_of_data(**kwargs)
        # 1、密码解密
        send_param = {
            "username": user_info.get("username"),
            "pwd": user_info.get("pwd"),
            "type": "username"
        }
        # todo 假设是Base64加密
        send_param["pwd"] = base64.b64decode(send_param["pwd"]).decode("utf-8")
        # 2、发送http请求进行登录操作
        res = keywords.send_HTTP_request(**send_param)
        # 保存token
        token = jsonpath(res.json(), "$..token")[0]
        gc.set_dict("token", token)
        return res

    @allure.step("随机获取数据库中的一条信息")
    def a_random_piece_of_data(self, **kwargs):
        """
        随机获取数据库中的一条信息
        Args:
            **kwargs: 包含数据库查询参数的字典，以下是可能的键值对说明
                query_content (list): 需要查询的字段列表，例如 ["id,username,pwd,gender"]。
                table (list): 需要查询的表名列表，例如 ["sxo_user"]。
                query_condition_where (list, optional): 查询的 WHERE 条件列表，例如 ["id > '100'", "username like 'ZYM%'"]。
                query_condition_group (list, optional): 查询的 GROUP BY 条件列表，例如 ["gender"]。
                query_condition_having (list, optional): 查询的 HAVING 条件列表，例如 ["count(gender) > 2"]。
                query_condition_order (list): 查询的 ORDER BY 条件列表，例如 ["rand()"]。
                query_condition_limit (list): 查询的 LIMIT 条件列表，例如 ["1"]。
                db_conf (dict): 数据库连接配置，包含以下键值对
                    host (str): 数据库主机地址，例如 "shop-xo.hctestedu.com"。
                    port (int): 数据库端口号，例如 3306。
                    user (str): 数据库用户名，例如 "api_test"。
                    password (str): 数据库用户密码，例如 "Aa9999!"。
                    db (str): 要连接的数据库名，例如 "shopxo_hctested"。
        """
        global user_info
        # query_content = "id,username,pwd,gender"  # 查询内容，如username,pwd
        query_condition = [self._build_condition(self.QUERY_CONTENT, "select", **kwargs),
                           self._build_condition(self.QUERY_TABLE, "from", **kwargs),
                           self._build_condition(self.QUERY_CONDITION_WHERE, "where", **kwargs),
                           self._build_condition(self.QUERY_CONDITION_GROUP, "group by", **kwargs),
                           self._build_condition(self.QUERY_CONDITION_HAVING, "having", **kwargs),
                           self._build_condition(self.QUERY_CONDITION_ORDER, "order by", **kwargs),
                           self._build_condition(self.QUERY_CONDITION_LIMIT, "limit", **kwargs)]
        sql = " ".join(query_condition).strip()

        db_context = {"cursorclass": cursors.DictCursor}
        db_context.update(kwargs.get(self.DB_CONFIG))
        if db_context and sql:
            connection = pymysql.connect(**db_context)
            cursor = connection.cursor()
            cursor.execute(sql)
            user_info = cursor.fetchone()

            gc.set_by_dict(user_info)
        return user_info

    @staticmethod
    def _build_condition(key, prefix, **kwargs):
        condition = kwargs.get(key, [])
        if condition:
            return f"{prefix} {' and '.join(condition)}"
        return ''

    @allure.step("提取MySQL数据库中的数据并存储")
    def ex_mysqlData(self, **kwargs):
        # context = read_yaml(CaseInfo.PATHOFCONTEXT + CaseInfo.CONTEXT, transform_list=False)
        db_context = {"cursorclass": cursors.DictCursor}
        db_context.update(gc.get_value("_database")["mysql001"])
        sql = kwargs.get("SQL")
        if db_context and sql:
            connection = pymysql.connect(**db_context)
            cursor = connection.cursor()
            cursor.execute(sql)
            res = cursor.fetchall()
            gc_will_load = {}
            Referencing_variables = kwargs.get(CaseInfo.REFERENCING_VARIABLES).split(",")
            for index, data in enumerate(res, 1):
                for j, val in enumerate(Referencing_variables):
                    gc_will_load[f'{Referencing_variables[j]}_{index}'] = data.get(Referencing_variables[j])

                # [{'id': 30926, 'username': 'ZYM_Q60yJD'}]:
                # data = {'id': 30926, 'username': 'ZYM_Q60yJD'}
                # j==1 时val = id
                gc.set_by_dict(gc_will_load)
                # print(res)
                cursor.close()
                connection.close()
        else:
            raise ValueError(f"数据错误，db_context:{db_context},sql:{sql}")


if __name__ == "__main__":
    sqlDriver = MysqlDriver()
    # send_param = {
    #     "query_content": ["id,username,pwd,gender"],
    #     "table": ["sxo_user"],
    #     "query_condition_where": ["id > '100'", "username like 'ZYM%'"],
    #     # "query_condition_group": ["gender"],
    #     # "query_condition_having": ["count(gender) > 2"],
    #     "query_condition_order": ["rand()"],
    #     "query_condition_limit": ["1"],
    #     MysqlDriver.DB_CONFIG: {"host": "shop-xo.hctestedu.com",
    #                             "port": 3306,
    #                             "user": "api_test",
    #                             "password": "Aa9999!",
    #                             "db": "shopxo_hctested"}
    #
    # }
    # sqlDriver.setup(**send_param)
    # print(user_info)
    pass
