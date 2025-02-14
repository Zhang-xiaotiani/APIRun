"""
Project: APIRun
File: setup
Created Date: 2025/2/9
Author: AILa
Email: zym822056523@gmail.com
Description: 
"""

import setuptools
import os

"""
打包成一个 可执行模块
"""
if os.path.exists("README.md"):
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
else:
    long_description = "Project description not available."

setuptools.setup(
    # 关于项目的介绍
    name="ZYM_APIRunner",
    version="0.0.1",
    author="AILa",
    author_email="zym822056523@gmail.com",
    description="接口自动化测试工具",
    license="GPLv3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Zhang-xiaotiani/",
    project_urls={
        "Bug Tracker": "https://github.com/Zhang-xiaotiani/",
        "Contact Us": "https://github.com/Zhang-xiaotiani/",
    },

    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ],
    # 需要安装的依赖 -- 工具依赖
    install_requires=[
        "allure-pytest==2.13.5",
        "Jinja2",
        "jsonpath",
        "pluggy",
        "pycparser",
        "PyMySQL",
        "PySocks",
        "pytest",
        "PyYAML",
        "pyyaml-include==1.3.1",
        "requests",
        "exceptiongroup",
        "jsonpath==0.82.2",
        "allure-pytest==2.13.5"
    ],
    packages=setuptools.find_packages(),
    package_data={'': ['*.*']},  # 默认只会加载py文件，设置加载所有的文件。
    python_requires=">=3.6",
    # 生成一个 可执行文件 例如 windows下面 .exe
    entry_points={
        'console_scripts': [
            # 可执行文件的名称=执行的具体代码方法
            'zym-apirun=apirun.main:run'
        ]
    },
    zip_safe=False
)
