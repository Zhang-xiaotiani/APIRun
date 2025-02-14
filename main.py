import pytest
import os
import subprocess

from core.CasePlugin import CasesPlugin
from util.CaseInfo import CaseInfo

# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    # os.chdir(os.path.dirname(os.path.abspath(__file__)))
    pytest_args = ["-s", "-v", "--capture=sys",  # 用于显示输出调试信息、 设置级别、打开实时输出
                   # "-n", "auto",
                   "--clean-alluredir",  # 清空alluredir中的历史数据
                   "--alluredir=allure-results",  # 执行过程的数据存放到allure-results中

                   # "--reruns=3",
                   # "--reruns-delay=1",
                   # r'--cases=D:\CodeLibrary\APIRun\cases\yaml_cases',
                   f"--type={CaseInfo.ALL_YAML}",
                   f"--cases={os.path.dirname(os.path.abspath(__file__))}\cases",
                   r'.\core\APITestRunner.py'
                   ]
    try:
        pytest.main(
            pytest_args,
            plugins=[CasesPlugin()]
        )
    except Exception as e:
        print("main函数错误：", e)
    # os.system("allure generate  -c -o  allure-report")  # 等于你在命令行里面执行 allure
    subprocess.run("allure generate -c -o allure-report", shell=True)

    # from allure_combine import combine_allure
    #
    # # combine_allure(测试报告的路径)
    # combine_allure("./allure-report")
