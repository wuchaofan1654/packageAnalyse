# -*- coding: utf-8 -*-
"""
Create by sandy at 11:44 02/04/2022
Description: ToDo
"""

dict_1 = {'sandy': {'age': 18, 'hobbit': '¥', 'ding': True}, 'Lily': {'age': 18, 'hobbit': '¥'}}

dict_1.update(lucy={'age': 19, 'ding': True})


class DeepUpdate(object):

    def __init__(self, _dict):
        self.result = _dict

    def update(self, key, value):
        if key not in self.result.keys():
            self.result[key] = value
            return self

        if isinstance(self.result[key], dict):
            if isinstance(value, dict):
                self.result[key].update(**value)
                return self

            self.result[key] = value
        return self


print(DeepUpdate(dict_1).update('sandy', {'age': 17, 'hobbit': '¥'}).update('Jack', '9999').result)
