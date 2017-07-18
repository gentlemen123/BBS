#! /usr/bin/env python3
# coding:utf-8
"""
爬虫主程序，调度各个模块！

@author：jingchengyou
@email：2505034080@qq.com
"""
import json
import os
import re
import sys

import gevent as gevent

from article_link_crawler import get_article_links
from webpage_crawler import get_page_url_number
from get_article import get_article_content
from article_analysis import analysis_article
from out_as_file import output_as_txt


def main():

    # 加载progress文件,防止从头再来
    try:
        with open('.progress.json', 'r') as f:
            progress = json.load(f)
        print('load process')
        print(progress)
    except IOError:
        progress = None

    if progress:
        try:
            num_pattern = re.compile(r'\d+')
            num_list = re.findall(num_pattern, progress['page'])
            page_number = num_list[-1]
        except IndexError as e:
            print(e)
            sys.exit(1)
    else:
        page_number = 1

    base_url = "http://www.xgbbs.net/xgbbs/index.asp?boardid=56"
    max_page = get_page_url_number(base_url)
    sub_url = "&TopicMode=0&List_Type=&Page="

    for num in range(page_number, max_page+1):
        page_url = base_url + sub_url + str(num)
        if get_article_links(page_url):
            break

    print('*'*5, "开始获取文章内容", '*'*5)
    greenlets = []
    for i in range(20):
        greenlets.append(gevent.spawn(get_article_content()))
    gevent.joinall(greenlets)

    print('*' * 5, "开始获取文章邮件", '*' * 5)
    analysis_article()

    print('*' * 5, "正在将数据输入format_data.txt", '*' * 5)
    output_as_txt()

    # 爬虫结束工作,删除过程记录文件
    print('delete progress')
    try:
        os.remove('.progress.json')
    except FileNotFoundError:
        pass
    print('done!')

    return

if __name__ == "__main__":
    main()
