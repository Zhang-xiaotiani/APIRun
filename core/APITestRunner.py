"""
Project: APIRun
File: APITestRunner
Created Date: 2025/2/10
Author: AILa
Email: zym822056523@gmail.com
Description:  pytest核心执行器
"""
import copy

import allure
import pytest

from core.globalContext import GlobalContext
from extend.KeyWords import KeyWords
from util.DynamicTitle import dynamicTitle
from util.VarRender import re_fresh
from util.CaseInfo import CaseInfo


class TestRunner:

    # @pytest.mark.parametrize(CaseInfo.CASE_INFO, cases_infos)
    def test_case_execute(self, case_info):
        gc = GlobalContext()
        keywords = KeyWords()
        # 测试用例的标题
        try:
            dynamicTitle(case_info)
            local_context = case_info.get(CaseInfo.CONTEXT, {})
            # 3.分解步骤
            steps = case_info.get(CaseInfo.STEPS, None)
            for step in steps:
                step_name = list(step.keys())[0]
                # allure.step(step_name)
                step_value = list(step.values())[0]

                # 更新前置接口获取的信息，如token
                context = copy.deepcopy(gc.get_all_value())
                context.update(local_context)
                step_value = eval(re_fresh(step_value, context))

                with allure.step(step_name):
                    step_func = step_value.get(CaseInfo.KEYWORDS, None)

                    try:
                        #  4、调用关键字函数---->反射
                        step_func = keywords.__getattribute__(step_func)
                        res = step_func(**step_value)

                    except Exception as e:
                        print(CaseInfo.RUN_ERROR, e)
                        assert False, f"核心执行器调用错误：{e}"

                    print("====step_func(**step_value)=========", res)

        except Exception as e:
            print(CaseInfo.RUN_ERROR, e)
            assert False, f"核心执行器调用错误：{e}"
        finally:
            print(CaseInfo.RUN_SUCCESS)


if __name__ == '__main__':
    pytest.main(['-vs', __file__])
