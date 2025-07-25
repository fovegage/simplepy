#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：codeline
@File    ：numpy_utils.py
@Author  ：fovegage
@Email   ：fovegage@gmail.com
@Date    ：2022/6/4 12:44
"""
from scipy.ndimage import shift
import numpy as np


def diff(data, method='div', x=-1, y=0):
    """
    错位运算
    :param data:
    :param method
    :param x:
    :param y:
    :return:
    """
    shift_data = shift(data, shift=[x, y], )
    print(shift_data)
    if method == 'div':
        return np.true_divide(shift_data, data)
    elif method == 'sub':
        return np.subtract(shift_data, data)


x = np.array([[1, 3, 6, 10], [1, 5, 6, 8]])
# print(x)
# print(np.diff(x, axis=0))
if __name__ == '__main__':
    print(diff(x, 'sub'))
