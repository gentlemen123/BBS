#! /usr/bin/env python3
# coding:utf-8
"""
将MongoDB中数据输出为文件！文件格式为txt

email:列表,经筛选,全局唯一
publish_time:字符串
title:字符串
telephone:列表,将组合成字符串

@author：jingchengyou
@email：2505034080@qq.com
"""
from data_storage import connection_mongodb
from config import name


def output_as_txt():
    """
    获取Mongodb中状态为one的文件,经处理后,改变状态为output
    注:经处理后,one状态必须为充分干净的数据
    :return:
    """
    col = connection_mongodb()
    total = col.count()
    i = total - col.find({'status': 'one'}).count()  # 已处理数量

    while True:
        articles = col.find_one(
            {'status': 'one'}
        )
        if not articles:
            break

        article_id = articles['article_id']
        email = articles['email']
        publish_time = articles['publish_time']
        title = articles['title']
        telephone = articles['telephone']

        # 将telephone组合成字符串
        if not telephone:
            telephone = None
        elif len(telephone) > 1:
            telephone = '/'.join(telephone)
        elif len(telephone) == 1:
            telephone = telephone[0]

        # 将一个帖子中的多个邮箱,分行输出
        for per in email:
            data_string = "{}\t{}\t{}\t{}\n".format(
                per, publish_time, title, telephone)
            with open('{}.txt'.format(name), mode='a+') as f:
                f.write(data_string)

            if data_string:
                col.find_one_and_update(
                    {'article_id': article_id},
                    {'$set': {
                        'status': "output"
                    }}
                )
                i += 1

        print("已写入比例:{} /{} ,比率:{:.2%}".format(i, total, i/total))
        if i/total == 1:
            print('done!')

    return


if __name__ == "__main__":
    output_as_txt()
