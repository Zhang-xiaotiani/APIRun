"""
Project: APIRun
File: YamlCaseParse
Created Date: 2025/2/10
Author: AILa
Email: zym822056523@gmail.com
Description: 该模块用于处理和解析 YAML 文件，读取相关的测试用例数据。
"""
import copy
import os.path

import allure
import yaml
from allure_commons.utils import uuid4

from core.globalContext import GlobalContext
from util.CaseInfo import CaseInfo
from util.GentraterString import generator_string

gc = GlobalContext()


# 读取并解析 YAML 文件内容
@allure.step("读取指定路径的 YAML 文件，并将其内容返回为 Python 对象")
def read_yaml(file_name, transform_list=True):
    """
    读取指定路径的 YAML 文件，并将其内容返回为 Python 对象。

    :param file_name: str，YAML 文件的路径。
    :param transform_list: bool，是否将返回的数据强制转换为列表（默认为 True）。
    :return: list 或 dict，返回读取的 YAML 文件内容。若参数 transform_list 为 True，返回的数据会被转换为列表。
    """
    with open(file_name, 'r', encoding='utf-8') as f:
        data = yaml.full_load(f)
    # 优化1：若data不是list，则修改为list
    if transform_list:
        data = data if isinstance(data, list) else [data]
    return data


# 从指定路径的 YAML 文件中读取上下文信息并加载到全局上下文中
@allure.step("从指定路径加载 context.yaml 文件并将其中的数据加载到全局上下文对象中。")
def load_context_from_yaml_to_global_context(path):
    """
    从指定路径加载 context.yaml 文件并将其中的数据加载到全局上下文对象中。

    :param path: str，YAML 文件所在的路径。
    :return: None
    """
    try:
        file_path = os.path.join(path, CaseInfo.CONTEXT)
        data = read_yaml(file_path, False)
        gc.set_by_dict(data)
        #     gc加入accounts
        gc.set_dict("account", generator_string("ZYM"))
        # print("generator_string====================", gc.get_all_value())

    except Exception as e:
        print(f"装载yaml文件失败---{str(e)}")


# 根据指定的路径加载 YAML 文件，并返回文件中的用例信息
@allure.step("加载指定路径下的所有 YAML 文件，并返回包含所有测试用例信息的列表。")
def load_yaml_by_path(path) -> list:
    """
    加载指定路径下的所有 YAML 文件，并返回包含所有测试用例信息的列表。

    :param path: str，文件所在的目录路径。
    :return: list，包含多个测试用例信息的列表，每个元素是一个 YAML 文件解析后的字典。
    """
    yaml_cases_infos = []
    # 1、获取context.yaml文件中的内容
    load_context_from_yaml_to_global_context(path)
    # 2.1、获取指定目录下的所有case文件
    file_names = []
    all_files = os.listdir(path)
    # 2.2、过滤满足要求的case
    for file in all_files:
        if file.endswith(".yaml") and file.split("_")[0].isdigit():
            file_num = int(file.split("_")[0])
            file_names.append((file_num, file))
    file_names.sort()
    file_names = [f[-1] for f in file_names]

    # 3、组合文件路径，读出文件
    for file_name in file_names:
        file_path = os.path.join(path, file_name)
        case_info = read_yaml(file_path, False)
        yaml_cases_infos.append(case_info)
    return yaml_cases_infos


# 解析 YAML 用例文件，生成用例信息字典
@allure.step("解析指定路径下的所有 YAML 用例文件，并返回包含用例名称和用例详细信息的字典。")
def yaml_case_parse(path: str = "") -> dict:
    """
    解析指定路径下的所有 YAML 用例文件，并返回包含用例名称和用例详细信息的字典。

    :param path: str，包含 YAML 用例文件的目录路径。
    :return: dict，包含用例名称和详细信息的字典，格式为 { 'case_infos': [...], 'case_names': [...] }
    """
    case_names = []
    case_infos = []
    # 1、加载所有 YAML 用例文件
    yaml_cases = load_yaml_by_path(path)
    #
    # 2、处理每个 YAML 用例数据
    for yaml_case in yaml_cases:
        print(yaml_case)
        ddts = yaml_case.get(CaseInfo.DDTS, {})

        # 无数据驱动
        if len(ddts) <= 0:
            # if True:
            # 获取用例描述，如果没有则生成唯一的 ID 作为名称
            case_name = yaml_case.get(CaseInfo.DESC, uuid4().__str__())
            yaml_case.update({CaseInfo.CASE_NAME: case_name})  # 在用例数据中添加用例名称

            case_names.append(case_name)  # 收集所有用例名称
            case_infos.append(yaml_case)  # 收集所有用例详细信息
        else:
            yaml_case.pop(CaseInfo.DDTS)
            # 有数据驱动
            for ddt in ddts:
                ddt_case = copy.deepcopy(yaml_case)

                # case_name
                case_name = f'{yaml_case.get(CaseInfo.DESC, uuid4().__str__())}_{ddt.get(CaseInfo.DESC, uuid4().__str__())}'
                case_names.append(case_name)

                # ddt信息加入ddt_case以便case_infos的append
                context = ddt_case.get(CaseInfo.CONTEXT, {})
                ddt_case.update(context)

                ddt_case.update({CaseInfo.CASE_NAME: case_name})
                ddt_case.update({CaseInfo.CONTEXT: ddt})

                case_infos.append(ddt_case)
    # 返回包含用例信息和名称的字典
    return {
        CaseInfo.CASE_INFOS: case_infos,
        CaseInfo.CASE_NAMES: case_names
    }


if __name__ == "__main__":
    # filename = "../cases/yaml_cases/yaml_login.yaml"
    # res = read_yaml(filename)
    # print(type(res),res)
    # print(load_context_from_yaml_to_global_context("D:\CodeLibrary\APIRun\cases\yaml_cases"))
    # print(load_yaml_by_path("D:\CodeLibrary\APIRun\cases\yaml_cases"))
    print(type(yaml_case_parse(r"D:\CodeLibrary\APIRun\cases\yaml_cases\test")["case_infos"]))
    pass
