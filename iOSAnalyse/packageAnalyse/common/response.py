# -*- coding: utf-8 -*-
"""
Create by sandy at 19:50 30/03/2022
Description: ToDo
"""
from rest_framework.response import Response


class SuccessResponse(Response):
    """
    标准响应成功的返回, SuccessResponse(data)或者SuccessResponse(data=data)
    (1)默认错误码返回200, 不支持指定其他返回码
    """

    def __init__(self, data=None, msg='success', status=None, template_name=None, headers=None, exception=False,
                 content_type=None):
        self.std_data = {
            "code": 200,
            "data": data,
            "msg": msg,
            "status": 'success'
        }
        super().__init__(self.std_data, status, template_name, headers, exception, content_type)

    def __str__(self):
        return str(self.std_data)


class ErrorResponse(Response):
    """
    标准响应错误的返回,ErrorResponse(msg='xxx')
    (1)默认错误码返回201, 也可以指定其他返回码:ErrorResponse(code=xxx)
    """

    def __init__(self, data=None, msg='error', code=201, status=None, template_name=None, headers=None,
                 exception=False, content_type=None):
        self.std_data = {
            "code": code,
            "data": data,
            "msg": msg,
            "status": 'error'
        }
        super().__init__(self.std_data, status, template_name, headers, exception, content_type)

    def __str__(self):
        return str(self.std_data)
