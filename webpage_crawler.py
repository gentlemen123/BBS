#! /usr/bin/env python3
# coding:utf-8
"""
论坛网页url爬取！

@author：jingchengyou
@email：2505034080@qq.com
"""
import requests
from lxml import html
from config import headers


def get_page_url(base_url):
    """
    从上一页得到下一页，无法确定最大页数的个情况
    :return: 一个字符串！返回下一个page的url
    """
    return


def get_page_url_number(base_url):
    """
    直接得到论坛页面数目
    :param base_url: 论坛首页url
    :return: 最大数目,int型
    """
    response = ""
    try:
        response = requests.get(base_url, headers=headers)
    except TimeoutError as e:
        print(e)
    else:
        if response.status_code != 200:
            print("code != 200")
            return False
        if "BBS北外星光站" not in response.text:
            print("not in the right page!")
            print("now in there:" + base_url)
            return False

    tree = html.fromstring(response.text)
    max_page = tree.xpath('//*[@id="showpage"]/a[12]/text()')[0]
    max_page = int(max_page.split('.')[-1])
    print('max page:', max_page)

    return max_page


if __name__ == "__main__":
    get_page_url_number("http://www.xgbbs.net/xgbbs/index.asp?boardid=56")
