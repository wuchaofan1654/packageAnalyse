# -*- coding: utf-8 -*-
"""
Create by sandy at 12:00 02/04/2022
Description: ToDo
"""


def deep_update(_dict, key, value):
    if key not in _dict.keys():
        _dict[key] = value
        return _dict

    if isinstance(_dict[key], dict):
        if isinstance(value, dict):
            _dict[key].update(**value)
            return _dict

        _dict[key] = value

    return _dict
