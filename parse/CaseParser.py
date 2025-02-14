"""
Project: APIRun
File: CaseParser
Created Date: 2025/2/12
Author: AILa
Email: zym822056523@gmail.com
Description: 用例解析器封装，根据传过来的参数，选择不同的解析器
"""
from pycparser.ply.yacc import restart

from parse.EXCELCaseParse import excel_case_parse
from parse.YamlCaseParse import yaml_case_parse
from util.CaseInfo import CaseInfo


def case_parser(case_type, case_dir):
    """

    :param case_type: 测试用例的类型
    :param case_dir: 测试用力的路径
    :return:
    """
    res = None
    if case_type == CaseInfo.ALL_YAML:
        res = yaml_case_parse(case_dir + "\yaml_cases")
    if case_type == CaseInfo.ALL_EXCEL:
        res = excel_case_parse(case_dir + "\excel_cases")
    if case_type == CaseInfo.ALL_CASE:
        res = yaml_case_parse(case_dir + "\yaml_cases")
        res_excel = excel_case_parse(case_dir + "\excel_cases")

        res["case_infos"].extend(res_excel["case_infos"])
        res["case_names"].extend(res_excel["case_names"])
    if res:
        case_infos = res.get("case_infos", [])
        case_names = res.get("case_names", [])
        return case_infos, case_names
    return {
        [], []
    }


if __name__ == "__main__":
    # p
    pass
