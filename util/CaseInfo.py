"""
Project: APIRun
File: CaseInfo
Created Date: 2025/2/11
Author: AILa
Email: zym822056523@gmail.com
Description: 
"""


class CaseInfo:
    ENCODING = "utf-8"
    PATH_OF_CONTEXT = r"D:\CodeLibrary\APIRun\cases\yaml_cases"
    CONTEXT =       "context.yaml"         # case公共信息文件
    CASE_INFO =     "case_info"            # case具体信息
    CASE_NAME =     "case_name"            # case名称
    CASE_INFOS =    "case_infos"           # 多个case 信息的列表
    CASE_NAMES =    "case_names"           # 多个case 名称的列表
    STEPS =         "steps"                # case步骤

    RUN_ERROR =     "出错啦！"                # 运行错误
    RUN_SUCCESS =   "执行结束！"              #  执行结束

    KEYWORDS = "关键字"
    DDTS = "ddts"
    DESC = "desc"

    #     yaml文件中的信息
    REFERENCING_VARIABLES = "引用变量"

    #     excel文件中的信息
    KEYWORDS_FILE_PATH = "extend/keywords.yaml"
    STORY_NAME = "storyName"   #一级模块
    FEATURE_NAME = "featureName"
    SECOND_LEVEL_MODULE = "二级模块"
    FIRST_LEVEL_MODULE = "一级模块"
    TYPE = "类型"
    VARIABLE = "变量"
    VARIABLE_DESCRIPTION='变量描述'
    VARIABLE_VALUE = '变量值'
    DATABASE = "数据库"
    TEST_CASE_TITLE = "测试用例标题"
    STEPS_DESCRIPTION = "步骤描述"
    PARAMS = "参数"

    # case解析器参数
    ALL_CASE  = "all"                    #执行所有yaml和excel文件测试用例
    ALL_YAML  = "yaml"                   #执行所有yaml文件测试用例
    ALL_EXCEL = "excel"                  #执行所有excel文件测试用例





if __name__ == "__main__":
    pass
