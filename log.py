#! /usr/bin/env python3
# coding:utf-8
"""
日志文件! 日志包含抓取信息

@author：jingchengyou
@email：2505034080@qq.com
"""
from config import name


def log(prompt, num, mode='a+'):
    """
     输出信息到日志文件
    :param prompt: 字符串, 在日志文件中作提示作用
    :param num: int, 要输入的数据
    :param mode: 字符串,输入文件是否覆盖重写
    :return:
    """
    with open('{}.txt'.format(name), mode=mode) as f:
        log_string = prompt + ': ' + num
        f.write(log_string)
    return

