# -*- coding: utf-8 -*-
# @Author : Hami

# 动态生成标题
import allure

from util.CaseInfo import CaseInfo


def dynamicTitle(CaseData):
    # pip install allure-pytest==2.13.5
    # 注意 这个caseinfo 是你参数化的数据给到的变量值。
    allure.dynamic.parameter(CaseInfo.CASE_INFO, "")

    # 如果存在自定义标题
    if CaseData.get(CaseInfo.CASE_NAME, None) is not None:
        # 动态生成标题
        allure.dynamic.title(CaseData[CaseInfo.CASE_NAME])

    if CaseData.get(CaseInfo.STORY_NAME, None) is not None:
        # 动态获取story模块名
        allure.dynamic.story(CaseData[CaseInfo.STORY_NAME])

    if CaseData.get(CaseInfo.FEATURE_NAME, None) is not None:
        # 动态获取feature模块名
        allure.dynamic.feature(CaseData[CaseInfo.FEATURE_NAME])

    if CaseData.get("remark", None) is not None:
        # 动态获取备注信息
        allure.dynamic.description(CaseData["remark"])

    if CaseData.get("rank", None) is not None:
        # 动态获取级别信息(blocker、critical、normal、minor、trivial)
        allure.dynamic.severity(CaseData["rank"])
