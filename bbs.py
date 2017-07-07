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

import re
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

    def get_next_page(self, curren_page_url):
        """输入当前url地址，获取下一页url地址"""
        text = requests.get(curren_page_url, headers=self.headers).text
        tree = html.fromstring(text)
        result = tree.xpath('/html/body/form/center/nobr/a[4]/@href')
        next_url = self.prefix_url+result[0]
        print(result)
        print(next_url)
        return next_url

    def enter_job_link(self, page_url):
        """输入网页url，反序输出该网页所有招聘信息url"""
        text = requests.get(page_url, headers=self.headers).text

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
        return article_link.reverse()

    def article_parse(self, article_link):
        """输入招聘信息url，招聘信息解析,输出邮箱 发帖时间 标题 电话形成钉列表"""
        infolist = []
        text = requests.get(article_link, headers=self.headers).text
        target_article_list = html.fromstring(text).xpath('//pre/text()')
        target_article = ""
        for article in target_article_list:
            target_article += article

        email_pattern = re.compile(r'[a-zA-Z0-9]+[.]?[\w]+@[0-9a-zA-z]+[.](com|cn)')
        time_pattern = re.compile(r'[0-9]+')
        tel_pattern = re.compile(r'1\d{10}')
        time_string = target_article.split('\n')[2]
        title = target_article.split('\n')[1].split(':')[1].strip()
        email = ""
        time_list = []
        tel = ""
        email_time = ""
        try:
            email = re.search(email_pattern, target_article).group()
            print(email)
        except Exception:
            print('-'*5 + "邮件格式匹配错误" + '-'*5)
            pass

        try:
            tel = re.search(tel_pattern, target_article).group()
            print(tel)
        except Exception:
            print('-' * 5 + "电话格式匹配错误" + '-' * 5)
            pass

        try:
            time_list = re.findall(time_pattern, time_string)
        except:
            print('-' * 5 + "时间格式匹配错误" + '-' * 5)
            pass

        if len(time_list) >= 3:
            email_time = time_list[0] + '/' + time_list[1] + '/' + time_list[2] + "  " + time_list[3] + ":" + time_list[4]
        if email != "":
            infolist.append(email)
            infolist.append(email_time)
            infolist.append(title)
            infolist.append(tel)
        return infolist

    def data_entry(self, infolist):
        """爬取信息录入到bbs.txt中"""
        with open('bbs.txt', mode='a') as f:
            f.write(str(infolist) + "\n")
        return


def main():
    search = JobSearch()
    # search.get_next_page(search.base_url)
    # print(search.enter_job_link(2))

    search.data_entry(search.article_parse('https://bbs.sjtu.edu.cn/bbscon,board,JobInfo,file,M.1499376489.A.html'))


if __name__ == '__main__':
    main()
