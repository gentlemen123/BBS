#! /usr/bin/env python3
# coding:utf-8
"""
日志文件! 日志包含抓取信息

@author：jingchengyou
@email：2505034080@qq.com
"""
from config import name
from data_storage import connection_mongodb


def log():
    """
     输出信息到日志文件
    :return:
    """
    col = connection_mongodb()

    one = col.find({'status': 'output'}).count()

    not_one= col.find({'status': 'not-one'}).count()
    not_email = col.find({'status': 'not-email'}).count()
    not_exit = col.find({'status': 'not-exit'}).count()

    done = one + not_one
    fetched = done + not_email
    not_done = fetched + not_exit

    p_string1 = '论坛招聘信息总数目: {}'.format(not_done)
    p_string2 = '其中抓取数目: {}, 文章不存在或抓取失败数目: {}, 抓取成功率:{:.2%}'.format(fetched, not_exit, fetched/not_done)
    p_string3 = '含有邮箱文章数目: {}, 不含有数目{}, 解析含有率:{:.2%}'.format(done, not_email, done/fetched)
    p_string4 = '所有邮箱中除重唯一数目: {}, 剩余邮箱数目{}'.format(one, not_one)
    p_string5 = '邮箱中除重唯一率: {:.2%}, 占抓取数目比率{:.2%}, 占论坛总数目比率{:.2%}'.format(one/done, one/fetched, one/not_done)

    with open('{}.txt'.format(name), mode='w+') as f:
        result = '{}\n{} ;\n{} ;\n{}\n{}\n'.format(p_string1, p_string2, p_string3, p_string4, p_string5)
        f.write(result)
    return

if __name__ == '__main__':
    log()


