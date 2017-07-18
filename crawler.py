#! /usr/bin/env python3
# coding:utf-8
"""
爬虫主程序，调度各个模块！

@author：jingchengyou
@email：2505034080@qq.com
"""
import requests

from article_link_crawler import get_article_links
from webpage_crawler import get_page_url_number
from get_article import get_article_content
from article_analysis import analysis_article
from out_as_file import output_as_txt


def main():
    base_url = "http://www.xgbbs.net/xgbbs/index.asp?boardid=56"
    max_page = get_page_url_number(base_url)
    sub_url = "&TopicMode=0&List_Type=&Page="

    for num in range(1, max_page+1):
        page_url = base_url + sub_url + str(num)
        if get_article_links(page_url):
            break

    print('*'*5, "开始获取文章内容", '*'*5)
    get_article_content()

    print('*' * 5, "开始获取文章邮件", '*' * 5)
    analysis_article()

    print('*' * 5, "正在将数据输入format_data.txt", '*' * 5)
    output_as_txt()

    return

if __name__ == "__main__":
    main()
