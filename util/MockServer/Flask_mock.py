"""
Project: APIRun
File: flask
Created Date: 2025/2/13
Author: AILa
Email: zym822056523@gmail.com
Description: 
"""
from flask import Flask, request, jsonify

import data

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, Flask!'


@app.route("/login", methods=["POST"], strict_slashes=False)
def login():
    # 以二进制数据获取数据

    # res = request.get_data()
    # res = request.data
    # print(res)
    # # # 以JSON数据获取数据
    # # res = request.get_json()
    # # res = request.json
    # # print(res)
    res = request.get_json()
    try:
        pass
        # username = res["username"]
        # pwd = res["pwd"]
    except Exception as e:
        return jsonify(data.LOGIN_ERROR)
    else:
        return jsonify(data.LOGIN_SUCCESS)
    return "欢迎来到登录页面"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
