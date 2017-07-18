#! /usr/bin/env python3
# coding:utf-8
"""
将MongoDB中数据输出为文件！文件格式为txt， 或xls

@author：jingchengyou
@email：2505034080@qq.com
"""
from data_storage import connection_mongodb


def output_as_txt():
    col = connection_mongodb()

    cursor = col.find({'status': 'fetched'})
    total = cursor.count()
    i = 1
    exist_emails = []  # 除重email,在整个mongodb数据库中
    for doc in cursor:
        contact = doc['contact']

        # email
        emails = contact.get('email')
        if emails:
            emails = [email.split()[0] for email in emails if email]
            remaining_emails = []
            for email in emails:
                if email in exist_emails:
                    continue
                else:
                    remaining_emails.append(email)
                    exist_emails.append(email)
        else:
            continue
        if remaining_emails:
            email_str = '/'.join(remaining_emails)
        else:
            continue

        # phone
        phones = contact.get('phone')
        if phones:
            phone_str = '/'.join(phones)
        else:
            phone_str = None

        # title
        title = str(doc['title'][0])

        # publish_time
        publish_time = doc['publishTime']

        # link
        # link = doc['link']

        data_str = '{}\t{}\t{}\t{}\n'.format(
            email_str, phone_str, publish_time, title
        )
        # print(data_str)
        print('{} / {}, {:.2f}%'.format(i, total, 100 * i / total))
        i += 1
        with open('./format_data.txt', 'a+') as f:
            f.write(data_str)


if __name__ == "__main__":
    output_as_txt()
