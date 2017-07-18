#! /usr/bin/env python3
# coding:utf-8
"""
解析mongodb中article字段的内容，获取邮箱、电话

@author：jingchengyou
@email：2505034080@qq.com
"""
import re

from data_storage import connection_mongodb


# 存在两个问题:1.article的值可能是列表形式  2.是否删除article的值
def analysis_article():
    col = connection_mongodb()

    total = col.count()
    i = 1
    while True:
        document = col.find_one({'status': 'done'})
        if not document:
            break
        try:
            id = document['id']
        except:
            print(document)
            _id = document['_id']
            col.find_one_and_update({'_id': _id}, {'$set': {'status': 'fail'}})
            continue
        try:
            text = str(document['article'])
            # link = document['link']
        except:
            print(id)
            col.find_one_and_update(
                {'id': id},
                {'$set': {
                    'status': 'not_done'
                }}
            )
            continue
        contact = {
            'phone': [],
            'email': []
        }

        while True:
            # telephone
            telephone_pattern = re.compile(r'0\d{2,3}-\d{7,8}|0\d{2,3}\d{7,8}|1[358]\d{9}|147\d{8}')
            # print(text)
            t = re.search(telephone_pattern, text)
            if t:
                contact['phone'].append(t.group())
                text = text.replace(t.group(), '')
            else:
                break

        while True:
            # email
            email_pattern = r'([A-Z_a-z_0-9.-]{1,64}@[a-z0-9-]{1,200}.{1,5}[a-z]{1,6})'
            e = re.search(email_pattern, text)
            if e:
                contact['email'].append(e.group(1))
                text = text.replace(e.group(1), '')
                continue

            email_pattern = r'([A-Z_a-z_0-9.-]{1,64}#[a-z0-9-]{1,200}.{1,5}[a-z]{1,6})'
            e = re.search(email_pattern, text)
            if e:
                contact['email'].append(e.group(1).replace('#', '@'))
                text = text.replace(e.group(1), '')
                continue

            email_pattern = r'([A-Z_a-z_0-9.-]{1,64} # [a-z0-9-]{1,200}.{1,5}[a-z]{1,6})'
            e = re.search(email_pattern, text)
            if e:
                contact['email'].append(e.group(1).replace(' # ', '@'))
                text = text.replace(e.group(1), '')
                continue

            email_pattern = r'([A-Z_a-z_0-9.-]{1,64} At [a-z0-9-]{1,200}.{1,5}[a-z]{1,6})'
            e = re.search(email_pattern, text)
            if e:
                contact['email'].append(e.group(1).replace(' At ', '@'))
                text = text.replace(e.group(1), '')
                continue

            email_pattern = r'([A-Z_a-z_0-9.-]{1,64}##[a-z0-9-]{1,200}.{1,5}[a-z]{1,6})'
            e = re.search(email_pattern, text)
            if e:
                contact['email'].append(e.group(1).replace('##', '@'))
                text = text.replace(e.group(1), '')
                continue

            email_pattern = r'([A-Z_a-z_0-9.-]{1,64}#_#[a-z0-9-]{1,200}.{1,5}[a-z]{1,6})'
            e = re.search(email_pattern, text)
            if e:
                contact['email'].append(e.group(1).replace('#_#', '@'))
                text = text.replace(e.group(1), '')
                continue

            email_pattern = r'([A-Z_a-z_0-9.-]{1,64} AT [a-z0-9-]{1,200}.{1,5}[a-z]{1,6})'
            e = re.search(email_pattern, text)
            if e:
                contact['email'].append(e.group(1).replace(' AT ', '@'))
                text = text.replace(e.group(1), '')
                continue

            email_pattern = r'([A-Z_a-z_0-9.-]{1,64} at [a-z0-9-]{1,200}.{1,5}[a-z]{1,6})'
            e = re.search(email_pattern, text)
            if e:
                contact['email'].append(e.group(1).replace(' at ', '@'))
                text = text.replace(e.group(1), '')
                continue

            break

        for email in contact['email']:
            if '\r' in email:
                email.replace()

        if contact['phone'] or contact['email']:
            # time.sleep(0.2)
            print('{} / {}, {:.2f}%'.format(i, total, 100*i/total))
            # print(contact)
            # time.sleep(1)
            col.find_one_and_update(
                {'id': id},
                {'$set': {
                    'contact': contact,
                    'status': 'fetched'
                }}
            )
        else:
            col.find_one_and_update(
                {'id': id},
                {'$set': {
                    'contact': {},
                    'status': 'fetched'
                }}
            )

        i += 1

    print("done")
    return


if __name__ == "__main__":
    analysis_article()
