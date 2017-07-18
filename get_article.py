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

from data_storage import connection_mongodb


def get_article_content():
    headers = {
        'Pragma': 'no-cache',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Referer': 'http://bbs.cloud.icybee.cn/board/JobInfo',
        'Connection': 'keep-alive',
        'Cache-Control': 'no-cache',
    }

    i = 0

    col = connection_mongodb()

    while True:
        article = col.find_one_and_update(
            {'status': 'not_done'},
            {'$set': {'status': 'ing'}}
        )
        if not article:
            break

        link = article['link']
        id = article['id']
        try:
            response = requests.get(link, headers=headers, timeout=60)
        except TimeoutError as e:
            print(e)
            # time.sleep(1)
            col.find_one_and_update(
                {'id': id},
                {'$set': {
                    'status': 'not_done',
                }}
            )
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
                col.delete_one({'link': link})
                i += 1
                continue
            # if '楼主' not in resp.text:
            #     print('not in the right page')
            #     print('current page:', resp.url)
            #     print('href:', href)
            #     sys.exit(1)

            tree = html.fromstring(response.text)
            article = tree.xpath("//div[@id='textstyle_1']/text()")
            # article = str(str(article).split())
            # comment_str = self.process_string(comment.text_content())
            # print(article)
            col.find_one_and_update(
                {'id': id},
                {'$set': {
                    'status': 'done',
                    'article': article
                }}
            )
            if i % 50 == 0:
                m = col.find({'status': 'done'}).count()
                m1 = col.find({'status': 'fetched'}).count()
                n = col.count()
                print('{} / {}, {:.1f}%'.format(m + m1, n, 100 * (m + m1) / n))
            i += 1
    print("done!")
    return


if __name__ == "__main__":
    get_article_content()
