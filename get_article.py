#! /usr/bin/env python3
# coding:utf-8
"""
获取mongodb中所有文章链接所对应的文章内容，并存储为article字段！

@author：jingchengyou
@email：2505034080@qq.com
"""

import requests
import sys

from lxml import html
from config import headers
from data_storage import connection_mongodb


def get_article_content():
    col = connection_mongodb()
    total = col.count()
    i = total - col.find({'status': 'not_done'}).count()

    while True:
        article = col.find_one(
            {'status': 'not_done'}
        )
        if not article:
            break

        link = article['article_link']
        article_id = article['article_id']
        try:
            response = requests.get(link, headers=headers, timeout=60)
        except TimeoutError as e:
            print(e)
            continue
        else:
            if response.status_code != 200:
                print('response.status_code:', response.status_code)
                print('link:', link)
                if '50' in str(response.status_code):
                    continue
                sys.exit(1)
            if '文章不存在' in response.text:
                print('article not exist')
                print('link:', link)
                col.find_one_and_update(
                    {'article_id': article_id},
                    {'$set': {
                        'status': 'not-exit'
                    }}
                )
                i += 1
                continue

            tree = html.fromstring(response.text)

            # 文章必须是字符串,此处还未处理
            article = tree.xpath("//div[@article_id='textstyle_1']/text()")

            if article:
                col.find_one_and_update(
                    {'article_id': article_id},
                    {'$set': {
                        'status': 'fetched',
                        'article': article
                    }}
                )
                i += 1
            else:
                col.find_one_and_update(
                    {'article_id': article_id},
                    {'$set': {
                        'status': 'not-exit'
                    }
                    }
                )
                i += 1

            print("文章爬取度:{}/{}, {:.2%}".format(i, total, i/total))
            if i/total == 1:
                print('done!')

    return


if __name__ == "__main__":
    get_article_content()
