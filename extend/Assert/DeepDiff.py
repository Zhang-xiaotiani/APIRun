"""
Project: APIRun
File: DeepDiff
Created Date: 2025/2/11
Author: AILa
Email: zym822056523@gmail.com
Description: 
"""
import allure
import deepdiff

from extend.Assert.AssertPublicParams import AssertPublicParams


class AssertDeepDiff:
    # @allure.step("全量断言")
    def assert_json_DeepDiff(self, **kwargs):
        actual = kwargs.get(AssertPublicParams.ACTUAL)
        expected = kwargs.get(AssertPublicParams.EXPECTED)
        exclude_paths = kwargs.get(AssertPublicParams.EXCLUDEPATHS)
        ignore_order = kwargs.get(AssertPublicParams.IGNOREORDER)
        ignore_string_case = kwargs.get(AssertPublicParams.IGNORESTRINGCASE)
        send_params = {"exclude_paths": exclude_paths,
                       "ignore_order": ignore_order,
                       "ignore_string_case": ignore_string_case}

        res = deepdiff.DeepDiff(actual, expected, **send_params)
        # print(res)
        assert not res, f"全量断言失败：{res}"


if __name__ == "__main__":
    # send_params = {"actual": {"key": "hello"},
    #                "expected": {"key": "HELLO"},
    #                "ignore_string_case": True
    #                }
    # print(AssertDeepDiff().assert_deep_diff(**send_params))  # True
    # print(deepdiff.DeepSearch(item="hello", obj={"key": {"key": "hello"}, "key1": "world"}))  # True
    pass
