#!/usr/bin/env python3
# coding:utf-8

"""
JobInfo(就业信息)爬取!
https://bbs.sjtu.edu.cn/bbsdoc?board=JobInfo

爬取内容：邮箱 电话 发帖时间 标题
主键：邮箱
爬取条件：相同邮箱，不同帖子，只取最新时间帖子

爬取步骤：
1 获取下一页url地址，并进入
2 进入每一条招聘信息
3 对招聘信息进行解析，取得邮箱，电话等四个信息，没有邮箱则直接退出
4 将爬取信息录入文件

数据存储形式：以dict的形式存入data.json
"""

import requests
from lxml import html
from bs4 import BeautifulSoup


class JobSearch(object):
    def __init__(self):
        self.base_url = "https://bbs.sjtu.edu.cn/bbsdoc?board=JobInfo"
        self.html = ""
        self.prefix_url = "https://bbs.sjtu.edu.cn/" # 前缀url地址
        self.headers = {
            'User-Agent': ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
                            '(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'),
            'Referer': 'https://easy.lagou.com/im/chat/index.htm',
            'Upgrade-Insecure-Requests': '1',
            'Accept-Language': 'zh,zh-CN;q=0.8,en;q=0.6,zh-TW;q=0.4'
        }

    def get_next_page(self, base_url):
        """输入当前url地址，获取下一页url地址"""
        self.base_url = base_url
        text = requests.get(self.base_url, headers=self.headers).text
        tree = html.fromstring(text)
        result = tree.xpath('/html/body/form/center/nobr/a[4]/@href')
        next_url = self.prefix_url+result[0]
        print(result)
        print(next_url)
        return next_url

    def enter_job_link(self, num=2):
        """输入每页遍历顺序，进入招聘信息"""
        text = requests.get(self.base_url, headers=self.headers).text

        soup = BeautifulSoup(text)
        article_link = []
        # print(type(article_link))

        for link in soup.find_all('a'):
            temp = link.get('href')
            if temp.startswith('bbscon,board,JobInfo,file,M.') or temp.startswith('bbscon?board=JobInfo&file'):
                article_link.append(temp)
                # print(temp)

        # print(article_link)
        # print(type(article_link))

        with open('templink.txt', mode='w') as f:
            for e in article_link:
                f.write(e+'\n')
        # tree = html.fromstring(text)
        # result = tree.xpath('/html/body/form/center/nobr/table[3]')
        # for i in result:
        #     print(i)
        #
        # print(type(result))
        # print(result)
        # #print(next_url)
        return article_link

    def article_parse(self):
        """招聘信息解析,获取邮箱 电话"""
        temp_url = "https://bbs.sjtu.edu.cn/bbscon,board,JobInfo,file,M.1499321577.A.html"
        text = requests.get(temp_url, headers=self.headers).text
        target_article = html.fromstring(text).xpath('//pre/text()')[1]
        print(target_article)
        title = target_article.split('\n')[1].split(':')[1].strip()
        print(title)
        with open('article.txt', mode='w') as f:
            f.write(target_article)
        return

    def data_entry(self):
        """爬取信息录入"""
        return


def main():
    search = JobSearch()
    # search.get_next_page(search.base_url)
    print(search.enter_job_link(2))
    # search.article_parse()


if __name__ == '__main__':
    main()
