#! /usr/bin/env python3
# coding:utf-8
"""
存储信息到MongoDB中！数据项有：id, email, telephone, publish_time, title, status

@author：jingchengyou
@email：2505034080@qq.com
"""
from pymongo import MongoClient


def insert_data(article_json):
    """
    插入数据
    :param article_json: json数据，包含id,link,title,publish_time,status
    :return:
    """
    db = MongoClient().get_database('beijingwaiguoyu')
    col = db.get_collection('articles')
    col.insert_one(article_json)
    return


def update_data():
    return


def del_data():
    return


def find_data(pattern_json):
    """
    在mongodb中找到和pattern_json匹配成功的文件
    :param pattern_json: json数据，查找的条件
    :return: boolean数据
    """
    db = MongoClient().get_database('beijingwaiguoyu')
    col = db.get_collection('articles')
    return col.find_one(pattern_json)

if __name__ == "__main__":
    insert_data()
