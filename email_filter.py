#! /usr/bin/env python3
# coding:utf-8
"""
过滤一个论坛内所有相同邮箱！只保留时间最新的邮箱

时间格式为:%Y-%m-%d %H:%M
@author：jingchengyou
@email：2505034080@qq.com
"""
import time

from data_storage import connection_mongodb


def email_filter():
    """
    1、拿到所有邮箱相同的帖子
    2、比对这些帖子的时间
    3、删除最新外的所有帖子
    注:默认状态为done的文件数据都为干净数据
    :return:
    """
    col = connection_mongodb()
    total = col.count()
    i = total - col.find({'status': 'done'}).count()  # 已处理数量

    while True:
        article = col.find_one({'status': 'done'})
        if not article:
            break

        article_id = article['article_id']
        email = article['email']
        publish_time = article['publish_time']

        same_email_list = col.find({'email': email})
        # 将每个相同邮箱的发表时间, 文章id取出,组合成元组, 放入info
        info = [(per['publish_time'], per['article_id']) for per in same_email_list]
        i += len(info)

        # new为所有相同邮箱中,发表时间最新的那一个的时间戳,默认值为publish_time
        # one为所有相同邮箱中,发表时间最新的那一个邮箱的文章id,亦是最后保留的The True One,默认值为email
        new = time.mktime(time.strptime(publish_time, "%Y-%m-%d %H:%M"))
        one = article_id
        for per in info:
            per_time = time.mktime(time.strptime(per[0], "%Y-%m-%d %H:%M"))
            if per_time > new:
                new = per_time
                one = per[1]
            else:
                col.find_one_and_update(
                    {'article_id': per[1]},
                    {'$set': {
                        'status': 'not-one'
                    }}
                )

        col.find_one_and_update(
            {'article_id': one},
            {'$set': {
                'status': 'one'
            }}
        )

        print("过滤完成度: {}/{}, {}".format(i, total, i/total))
        if i/total:
            print("done!")

    return


if __name__ == "__main__":
    email_filter()
