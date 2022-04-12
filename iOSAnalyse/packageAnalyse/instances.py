# -*- coding: utf-8 -*-
"""
Create by sandy at 10:53 12/04/2022
Description: ToDo
"""
from typing import Text, Dict, List
from pydantic import BaseModel


class SingleCompareResult(BaseModel):
    module_name: Text = ''
    pk1_module_size: int = 0
    pk2_module_size: int = 0
    diff_size: int = 0

    def calculate_diff(self):
        self.diff_size = self.pk2_module_size - self.pk1_module_size
        return self


class CompareResult(BaseModel):
    pk1_publish: Dict = {}
    pk2_publish: Dict = {}
    results: List[SingleCompareResult] = []

    def sort_by_diff(self):
        self.results = sorted(self.results, key=lambda result: result.diff_size, reverse=True)
        return self

