import copy
from typing import Any

import allure
from typing import Any

import jsonpath

from core.globalContext import GlobalContext
from extend.Assert.AssertPublicParams import AssertPublicParams


class AssertComparators:

    @staticmethod
    @allure.step("断言实际值等于预期值")
    def assert_equal(actual: Any, expected: Any, **kwargs) -> bool:
        """
        判断两个值是否相等。
        """
        return actual == expected

    @staticmethod
    @allure.step("断言实际值不等于预期值")
    def assert_not_equal(actual: Any, expected: Any, **kwargs) -> bool:
        """
        判断两个值是否不相等。
        """
        return actual != expected

    @staticmethod
    @allure.step("断言实际值为真（True）")
    def assert_true(actual: bool, **kwargs) -> bool:
        """
        判断实际值是否为真（True）。
        """
        return bool(actual) is True

    @staticmethod
    @allure.step("断言实际值为假（False）")
    def assert_false(actual: bool, **kwargs) -> bool:
        """
        判断实际值是否为假（False）。
        """
        return bool(actual) is False

    @staticmethod
    @allure.step("断言实际值为 None")
    def assert_is_none(actual: Any, **kwargs) -> bool:
        """
        判断实际值是否为 None。
        """
        return actual is None

    @staticmethod
    @allure.step("断言实际值不为 None")
    def assert_is_not_none(actual: Any, **kwargs) -> bool:
        """
        判断实际值是否不为 None。
        """
        return actual is not None

    @staticmethod
    @allure.step("断言项在集合中")
    def assert_in(item: Any, collection: Any, **kwargs) -> bool:
        """
        判断某项是否包含在集合中。
        """
        try:
            return item in collection
        except TypeError:
            raise TypeError("The collection parameter must be an iterable type.")

    @staticmethod
    @allure.step("断言项不在集合中")
    def assert_not_in(item: Any, collection: Any, **kwargs) -> bool:
        """
        判断某项是否不包含在集合中。
        """
        try:
            return item not in collection
        except TypeError:
            raise TypeError("The collection parameter must be an iterable type.")

    @staticmethod
    @allure.step("断言集合为空")
    def assert_is_empty(collection: Any, **kwargs) -> bool:
        """
        判断集合是否为空。
        """
        try:
            return len(collection) == 0
        except TypeError:
            raise TypeError("Collection must be an iterable type.")

    @staticmethod
    @allure.step("断言集合不为空")
    def assert_is_not_empty(collection: Any, **kwargs) -> bool:
        """
        判断集合是否不为空。
        """
        try:
            return len(collection) > 0
        except TypeError:
            raise TypeError("Collection must be an iterable type.")

    @staticmethod
    @allure.step("断言目标包含子字符串或元素（深度搜索={deep_search}）")
    def assert_contain(substring: Any, target: Any, deep_search: bool = False, **kwargs) -> bool:
        """
        判断目标是否包含指定子字符串或元素。
        """
        if deep_search:
            def deep_search_contain(sub, obj):
                # 检查当前层是否匹配
                if isinstance(obj, str) and isinstance(sub, str):
                    if sub in obj:
                        return True
                else:
                    if sub == obj:
                        return True

                # 处理字典的键值对包含
                if isinstance(sub, dict) and isinstance(obj, dict):
                    # 检查obj是否包含sub的所有键值对
                    for k, v in sub.items():
                        if k not in obj:
                            return False
                        if not deep_search_contain(v, obj[k]):
                            return False
                    return True

                # 递归检查子元素
                if isinstance(obj, dict):
                    for key, value in obj.items():
                        if deep_search_contain(sub, key) or deep_search_contain(sub, value):
                            return True
                elif isinstance(obj, list):
                    for item in obj:
                        if deep_search_contain(sub, item):
                            return True
                return False

            return deep_search_contain(substring, target)
        else:
            try:
                if isinstance(substring, dict):
                    for key, value in substring.items():
                        if key in target and value == target.get(key):
                            return True
                    return False
                else:
                    return substring in target
            except TypeError:
                raise TypeError("Target must be an iterable type.")

    @staticmethod
    @allure.step("断言目标不包含子字符串或元素（深度搜索={deep_search}）")
    def assert_not_contain(substring: Any, target: Any, deep_search: bool = False, **kwargs) -> bool:
        """
        判断目标是否不包含指定子字符串或元素。
        """
        if deep_search:

            def deep_search_not_contain(substring_, target_):
                # 检查当前层是否匹配
                current_match = False
                if isinstance(target_, str) and isinstance(substring_, str):
                    current_match = substring_ in target_
                else:
                    current_match = (substring_ == target_)

                # 处理字典的键值对包含
                if not current_match and isinstance(substring_, dict) and isinstance(target_, dict):
                    current_match = True
                    for k, v in substring_.items():
                        if k not in target_ or deep_search_not_contain(v, target_[k]):
                            current_match = False
                            break

                if current_match:
                    return True

                # 递归检查子元素
                if isinstance(target_, dict):
                    for key, value in target_.items():
                        if deep_search_not_contain(substring_, key) or deep_search_not_contain(substring_, value):
                            return True
                elif isinstance(target_, list):
                    for item in target_:
                        if deep_search_not_contain(substring_, item):
                            return True
                return False

            return not deep_search_not_contain(substring, target)
        else:
            try:
                if isinstance(substring, dict):
                    for key, value in substring.items():
                        if key in target and value == target.get(key):
                            return False
                    return True
                else:
                    return substring not in target
            except TypeError:
                raise TypeError("Target must be an iterable type.")

    @staticmethod
    # @allure.step("断言当前文本")
    def assert_text_comparators(**kwargs):
        """
        封装断言以进行不同的比较操作。
        参数:
        value (Any): 要比较的值。
        expected (Any): 预期的值。
        op_str (str): 操作符的字符串表示（如 '>', '<', '==' 等）。
        message (str, optional): 自定义的错误消息。
        返回:
        None: 如果断言成功，则不返回任何内容。
        引发:
        AssertionError: 如果断言失败。
        """
        comparators = {
            '>': lambda a, b: a > b,
            '<': lambda a, b: a < b,
            '==': lambda a, b: a == b,
            '>=': lambda a, b: a >= b,
            '<=': lambda a, b: a <= b,
            '!=': lambda a, b: a != b,
        }
        actual = kwargs.get(AssertPublicParams.ACTUAL, None)
        expected = kwargs.get(AssertPublicParams.EXPECTED, None)
        op_str = kwargs.get(AssertPublicParams.OP_STR, None)
        message = kwargs.get(AssertPublicParams.MESSAGE, None)
        if op_str not in comparators:
            raise ValueError(f"assert方式错误：{op_str}")
        else:
            try:
                if not comparators.get(op_str)(actual, expected):
                    # raise AssertionError(f"出错啦！actual={actual},expected={expected}")
                    raise AssertionError(message if message else f"出错啦！actual={actual},expected={expected}")
            except Exception as e:
                raise AssertionError(f"出错啦！actual={actual},expected={expected}")

    # TODO: 扩展 - JSOND断言方法
    @allure.step("参数数据：JSOND断言文本内容")
    def assert_json_comparators(self, **kwargs):
        """
        封装断言以进行不同的比较操作。

        参数:
        value (Any): 要比较的jsonPath值。
        expected (Any): 预期的值。
        op_str (str): 操作符的字符串表示（如 '>', '<', '==' 等）。
        message (str, optional): 自定义的错误消息。

        返回:
        None: 如果断言成功，则不返回任何内容。

        引发:
        AssertionError: 如果断言失败。
        """
        comparators = {
            '>': lambda a, b: a > b,
            '<': lambda a, b: a < b,
            '==': lambda a, b: a == b,
            '>=': lambda a, b: a >= b,
            '<=': lambda a, b: a <= b,
            '!=': lambda a, b: a != b,
        }

        message = kwargs.get("MESSAGE", None)

        if kwargs["OP_STR"] not in comparators:
            raise ValueError(f"没有该操作方式: {kwargs['OP_STR']}")

        # 通过jsonpath获取对应的数据
        # 获取响应数据
        response = GlobalContext().get_value("current_response").json()
        ex_data = jsonpath.jsonpath(response, kwargs['VALUE'])[0]  # 默认就取第一个

        if not comparators[kwargs['OP_STR']](ex_data, kwargs["EXPECTED"]):
            if message:
                raise AssertionError(message)
            else:
                raise AssertionError(f"{ex_data} {kwargs['OP_STR']} {kwargs['EXPECTED']} 失败")


# 示例用法：
if __name__ == "__main__":
    try:
        # print(AssertComparators.assert_text_comparators(actual="hello", expected="hello world", op_str="==", message="出错啦"))  # True

        # assert_contain 用法
        # print(AssertComparators.assert_contain("hello", "hello world", deep_search=True))  # True
        # print(AssertComparators.assert_contain("hello", ["hello", "world"], deep_search=True))  # True
        # print(AssertComparators.assert_contain("hello", [["hello", "heools"], "world"], deep_search=True))  # True
        # print(AssertComparators.assert_contain("hello", [["hello", "heools"], "world"], deep_search=False))  # False
        # print(AssertComparators.assert_contain({"key": "hello"}, {"key": {"key": "hello"}, "key1": "world"},deep_search=True))  # True
        # print(AssertComparators.assert_contain({"key": "hello"}, {"key": {"key": "hello"}, "key1": "world"}))  # False
        # print(AssertComparators.assert_contain("hello", {"key": "hello", "key1": "world"}, deep_search=True))  # True
        # print(AssertComparators.assert_contain({"key": "hello"}, {"key": "hello", "key1": "world"}, deep_search=True))  # True
        # print(AssertComparators.assert_contain("hello", {"key": ["hello", "world"]}, deep_search=True))  # True

        # print(AssertComparators.assert_not_contain("hello", "hello world", deep_search=True))  # True
        # print(AssertComparators.assert_not_contain("hello", ["hello", "world"], deep_search=True))  # True
        # print(AssertComparators.assert_not_contain("hello", [["hello", "heools"], "world"], deep_search=True))  # True
        # print(AssertComparators.assert_not_contain("hello", [["hello", "heools"], "world"], deep_search=False))  # False
        # print(AssertComparators.assert_not_contain({"key": "hello"}, {"key": {"key": "hello"}, "key1": "world"}, deep_search=True))  # True
        # print(AssertComparators.assert_not_contain({"key": "hello"}, {"key": {"key": "hello"}, "key1": "world"}))  # False
        # print(AssertComparators.assert_not_contain("hello", {"key": "hello", "key1": "world"}, deep_search=True))  # True
        # print(AssertComparators.assert_not_contain({"key": "hello"}, {"key": "hello", "key1": "world"}, deep_search=True))  # True
        # print(AssertComparators.assert_not_contain("hello", {"key": ["hello", "world"]}, deep_search=True))  # False

        # # assert_is_empty 用法
        # print(Assert.assert_is_empty([]))  # True
        # print(Assert.assert_is_empty([1, 2]))  # False
        #
        # # assert_is_not_empty 用法
        # print(Assert.assert_is_not_empty([1]))  # True
        # print(Assert.assert_is_not_empty([]))  # False
        # test = {"key": "hello"}
        # cop = copy.deepcopy(test)
        # print(Assert.assert_equal(test, cop))  # True
        pass

    except AssertionError as e:
        print(f"Assertion failed: {e}")
