#! /usr/bin/env python3
# coding:utf-8
"""
解析mongodb中article字段的内容，获取邮箱、电话

@author：jingchengyou
@email：2505034080@qq.com
"""
import re

from data_storage import connection_mongodb


def analysis_article():
    col = connection_mongodb()
    total = col.count()
    i = total - col.find({'status': 'fetched'}).count()
    while True:
        articles = col.find_one({'status': 'fetched'})
        if not articles:
            break

        article_id = articles['article_id']
        article = articles['article']

        # email:数组
        email_pattern = re.compile(r'[0-9a-zA-Z]+[.0-9a-zA-Z_-]'
                                   r'+@[0-9a-zA-Z_-]+.[a-zA-Z0-9]+.?[a-zA-Z0-9]+.?[a-zA-Z0-9]+')
        result_email = re.findall(email_pattern, article)
        if result_email:
            temp = set(result_email)
            email = list(temp)
        else:
            email = None

        if not email:
            col.find_one_and_update(
                {'article_id': article_id},
                {'$set': {
                    'status': 'not-email'
                }}
            )
            i += 1
            continue

        # 电话:数组
        telephone_pattern = re.compile(r'0\d{2,3}-\d{7,8}|0\d{2,3}\d{7,8}|1[358]\d{9}|147\d{8}')
        result_phone = re.findall(telephone_pattern, article)
        if result_phone:
            telephone = result_phone
        else:
            telephone = None

        col.find_one_and_update(
            {'article_id': article_id},
            {
                '$set': {
                    'email': email,
                    'telephone': telephone,
                    'status': 'done',
                }
            }
        )
        i += 1

        print("文章解析完成度:{} /{}, {:.2%}".format(i, total, i / total))
        if i / total == 1:
            print('done!')

    return


if __name__ == "__main__":
    analysis_article()
