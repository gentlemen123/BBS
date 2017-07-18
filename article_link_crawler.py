#! /usr/bin/env python3
# coding:utf-8
"""
爬取论坛一个页面中所有文章链接！

@author：jingchengyou
@email：2505034080@qq.com
"""

import sys
import json
import time
import requests
from lxml import html

from data_storage import find_data
from data_storage import insert_data


def get_article_links(page_url):
    """
    获取一个论坛页面所有普通主题的文章链接,标题,发表时间!
    将值存入mongodb中
    :param page_url: 论坛页面url
    :return:
    """
    print("\ngo to page:", page_url)
    with open(".progress.json", "w+") as f:
        json.dump({
            'page': page_url
        }, f)

    headers = {
        'Pragma': 'no-cache',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/57.0.2987.133 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Referer': 'http://bbs.cloud.icybee.cn/board/JobInfo',
        'Connection': 'keep-alive',
        'Cache-Control': 'no-cache',
    }

    try:
        a = time.time()  # 发出请求的时间
        response = requests.get(page_url, headers=headers)
        b = time.time()  # 请求结束的时间
        print("一次请求所需时间:",b-a)  # 输出一次请求所需的时间
    except TimeoutError as e:
        print(e)
        sys.exit(1)
    except ConnectionError as e:
        print(e)
        print("页面url出错")
    else:
        if response.status_code != 200:
            print('code != 200')
            sys.exit(1)
        if "招聘|兼职" not in response.text:
            print('not in the right page')
            print('current page:', page_url)
            sys.exit(1)

        tree = html.fromstring(response.text) # "//table[@class='mainbox tableborder']/tbody/tr[@class='trout']"
        article_links = tree.xpath("//form/table[@class='mainbox tableborder']/tr[@onmouseover]")
        # print(article_links)
        print("count:", len(article_links))
        for article_link in article_links:
            article_link = html.fromstring(html.tostring(article_link))

            # 文章最后回复时间 因为page内文章按照回复时间降序排列
            update_time = article_link.xpath("//td[5]/a/text()")[0]
            if '2017-7-5' in update_time:
                print(update_time)
                print('done')
                return True  # 如果爬取的起止时间出现,则返回True,停止爬取

            # 文章发表时间
            publish_time = article_link.xpath('//td[3]/a/text()')[1].strip()
            if ':' not in publish_time:
                p = publish_time.split('-')
                year = p[0]
                month = p[1]
                day = p[2]
                if year != '2017':
                    continue
                if int(month) < 7 and int(day) < 5:
                    continue
            else:
                publish_time = '2017-07-17'

            link = article_link.xpath("//td[2]/a/@href")
            title = article_link.xpath("//td[2]/a/text()")
            if link and title:
                link = link[0]
                title = title[0].split()
            else:
                break
            id = link.split('=')[-1]
            link = 'http://www.xgbbs.net/xgbbs/' + link
            article_json = {
                'id': id,
                'link': link,
                'title': title,
                'publishTime': publish_time,
                'status': 'not_done'
            }
            if not find_data({'id': id}):
                insert_data(article_json)
    return False


if __name__ == "__main__":
    page_url = "http://www.xgbbs.net/xgbbs/index.asp?boardid=56&TopicMode=0&List_Type=&Page=1"
    get_article_links(page_url)
