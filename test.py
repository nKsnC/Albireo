#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
单元测试

@File    :   test.py
@Time    :   2020/10/06 19:20:12
@Author  :   snc 
"""

import unittest
import requests


class ApiTest(unittest.TestCase):
    def tearDown(self):
        # 每个测试用例执行之后做操作
        print('***')

    def setUp(self):
        # 每个测试用例执行之前做操作
        print('***')

    @classmethod
    def tearDownClass(self):
        # 必须使用 @ classmethod装饰器, 所有test运行完后运行一次
        print('---测试结束---')

    @classmethod
    def setUpClass(self):
        # 必须使用@classmethod 装饰器,所有test运行前运行一次
        print('---开始测试---')

    def test_my_bangumi(self):
        headers = {
            'Content-Type': 'application/json',
        }
        res = requests.get("http://127.0.0.1:5000/api/home/my_bangumi")
        assert res.status_code == 200
