"""
Project: APIRun
File: CasePlugin
Created Date: 2025/2/12
Author: AILa
Email: zym822056523@gmail.com
Description: pytest插件类

"""
from parse.CaseParser import case_parser
from util.CaseInfo import CaseInfo


class CasesPlugin:
    def pytest_addoption(self, parser):
        """
        做配置项
        :param parser:
        :return:
        """
        parser.addoption("--type", action='store', default=CaseInfo.ALL_CASE, help='测试用例的类型，all:全部、ymal:yaml测试文件、excel：excel测试用例')
        parser.addoption("--cases", action='store', default='./cases', help='测试用例的目录')

    # 调用测试用例，并做参数化
    def pytest_generate_tests(self, metafunc):
        case_type = metafunc.config.getoption('type')
        cases_dir = metafunc.config.getoption('cases')
        # 调用测试用例的解析器
        case_infos, case_names = case_parser(case_type, cases_dir)
        if "case_info" in metafunc.fixturenames:
            metafunc.parametrize("case_info", case_infos, ids=case_names)

    # 转码
    def pytest_collection_modifyitems(self, items):
        for item in items:
            item.name = item.name.encode("utf-8").decode("unicode_escape")
            item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")


if __name__ == "__main__":
    pass
