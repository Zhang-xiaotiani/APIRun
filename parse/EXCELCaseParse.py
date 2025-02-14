"""
Project: APIRun
File: EXCELCaseParse
Created Date: 2025/2/10
Author: AILa
Email: zym822056523@gmail.com
Description:  excel文件处理
"""
from uuid import uuid4

import allure
import pandas as pd

from util.CaseInfo import CaseInfo

import json
import os
import ast
import pandas as pd
import yaml

from core.globalContext import GlobalContext


def read_excel(filename, ):
    df = pd.read_excel(filename)
    # print(df)
    # 转成字典
    row_to_dict = df.to_dict(Series='records')
    # 转成列表
    # row_to_list = df.values.tolist()
    # print(row_to_list)
    return row_to_dict


# {'_database': {'mysql001': {'host': 'shop-xo.hctestedu.com', 'port': 3306, 'user': 'api_test', 'password': 'Aa9999!', 'db': 'shopxo_hctested'}}, 'URL': 'http://shop-xo.hctestedu.com', 'USERNAME': 'hami'}

# 优化读出excel文件的函数（传路径）----读出context.yaml中的内容并存到全局的dict中
def load_context_from_excel_to_global_context(folder_path):  # D:\Apirun2411\examples\yaml_testcase
    try:
        excel_file_path = os.path.join(folder_path, 'context.xlsx')
        df = pd.read_excel(excel_file_path)
        data = {'_database': {}}
        for index, row in df.iterrows():

            # 类型= 变量
            if row[CaseInfo.TYPE] == CaseInfo.VARIABLE:
                data[row[CaseInfo.VARIABLE_DESCRIPTION]] = row[CaseInfo.VARIABLE_VALUE]

            # 类型 = 数据库
            if row[CaseInfo.TYPE] == CaseInfo.DATABASE:
                db_name = row[CaseInfo.VARIABLE_DESCRIPTION]
                db_config = json.loads(row[CaseInfo.VARIABLE_VALUE])
                data['_database'][db_name] = db_config
        # print("加载context.excel内容:", data)
        if data:
            GlobalContext().set_by_dict(data)

    except  Exception as e:
        print(f"装载excel文件失败：{str(e)}")


def load_excel_files(folder_path):
    """
    优化读出yaml文件的函数--读出指定目录下的所有满足“数据_名称.yaml”这个条件的所有文件名，
    组合成多个测试用例
    """
    excel_case_infos = []
    # a.调用存储context.excel的函数
    load_context_from_excel_to_global_context(folder_path)
    # b.获得指定目录下的所有满足条件文件名
    file_names = []
    allfiles = os.listdir(folder_path)
    for f in allfiles:
        if f.endswith('.xlsx') and f.split('_')[0].isdigit():
            file_number = int(f.split('_')[0])
            file_names.append((file_number, f))
    # file_names = 【【1，filename1】,【2，filename2】】
    file_names.sort()
    file_names = [f[-1] for f in file_names]
    # print(file_names)
    current_dir = os.path.abspath(os.path.dirname(__file__))
    parent_dir = os.path.dirname(current_dir)
    keywords_file_path = os.path.join(parent_dir, CaseInfo.KEYWORDS_FILE_PATH)
    keywords_info = {}
    with open(keywords_file_path, 'r', encoding=CaseInfo.ENCODING) as f:
        keywords_info = yaml.full_load(f)

    # c.组合文件路径并读出测试用例#D:\Apirun2411\examples\yaml_testcase\    yaml_00141login.excel
    for file_name in file_names:
        file_path = os.path.join(folder_path, file_name)
        data = pd.read_excel(file_path, sheet_name=0)
        # 把data中的所有的nan，取非空值
        data = data.where(data.notnull(), None)
        # 把excel转为字典
        data = data.to_dict(orient="records")
        # 定义放一条测试用例的变量
        current_test_case = None
        for row in data:
            # print(row)
            # 处理测试用的标题
            # pd.notna():内容为空时，返回False，否则返回为True。！！！！！！！！合并单元格只有第一次读取时非空
            if pd.notna(row[CaseInfo.TEST_CASE_TITLE]):
                if current_test_case is not None:
                    excel_case_infos.append(current_test_case)

                current_test_case = {
                    CaseInfo.DESC: row[CaseInfo.TEST_CASE_TITLE],
                    # CaseInfo.FEATURE_NAME: row[CaseInfo.FIRST_LEVEL_MODULE],
                    # CaseInfo.STORY_NAME: row[CaseInfo.SECOND_LEVEL_MODULE],
                    CaseInfo.STEPS: []
                }
            # 处理steps
            steps = {
                row[CaseInfo.STEPS_DESCRIPTION]: {
                    CaseInfo.KEYWORDS: row[CaseInfo.KEYWORDS]
                }
            }
            # 处理参数
            param = []
            for key, value in row.items():
                if CaseInfo.PARAMS in key:
                    try:
                        value = ast.literal_eval(value)
                    except Exception as e:
                        pass
                    param.append(value)
            # 对应的KEY和value进行对应
            dict_param = {k: v for k, v in zip(keywords_info[row[CaseInfo.KEYWORDS]], param)}
            # 组装好的参数就要放到步骤steps中
            steps[row[CaseInfo.STEPS_DESCRIPTION]].update(dict_param)
            # 再把steps加到测试用例
            current_test_case[CaseInfo.STEPS].append(steps)
        if current_test_case is not None:
            excel_case_infos.append(current_test_case)
        x = len(excel_case_infos)
    return excel_case_infos


@allure.step("解析指定路径下的所有 excel 用例文件，并返回包含用例名称和用例详细信息的字典。")
def excel_case_parse(path: str = "") -> dict:
    """
    解析指定路径下的所有 YAML 用例文件，并返回包含用例名称和用例详细信息的字典。

    :param path: str，包含 YAML 用例文件的目录路径。
    :return: dict，包含用例名称和详细信息的字典，格式为 { 'case_infos': [...], 'case_names': [...] }
    """
    case_names = []
    case_infos = []
    # 1、加载所有 YAML 用例文件
    excel_cases = load_excel_files(path)
    #
    # 2、处理每个 YAML 用例数据
    for excel_case in excel_cases:
        # print(yaml_case)

        case_name = excel_case.get(CaseInfo.DESC, uuid4().__str__())
        excel_case.update({CaseInfo.CASE_NAME: case_name})  # 在用例数据中添加用例名称

        case_names.append(case_name)  # 收集所有用例名称
        case_infos.append(excel_case)  # 收集所有用例详细信息

    # 返回包含用例信息和名称的字典
    return {
        CaseInfo.CASE_INFOS: case_infos,
        CaseInfo.CASE_NAMES: case_names
    }


if __name__ == "__main__":
    file_path = r"D:\CodeLibrary\APIRun\cases\excel_cases"
    # excel = read_excel(file)
    # print(excel)
    # print(load_excel_files(file_path))
    print(excel_case_parse(file_path))
    pass
