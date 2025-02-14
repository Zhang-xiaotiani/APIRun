"""
Project: APIRun
File: test001
Created Date: 2025/2/13
Author: AILa
Email: zym822056523@gmail.com
Description: 
"""
import requests

url = 'http://127.0.0.1:5000/login'
data = {'a': 1, 'c': 2}
res = requests.post(url=url, json=data)
print(res.text)
