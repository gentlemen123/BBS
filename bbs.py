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
import datetime
import json
import os
import re
import requests
from lxml import html
from bs4 import BeautifulSoup


class JobSearch(object):
    def __init__(self):
        self.base_url = "https://bbs.sjtu.edu.cn/bbsdoc?board=JobInfo"
        self.html = ""
        self.prefix_url = "https://bbs.sjtu.edu.cn/"  # 前缀url地址
        self.headers = {
            'User-Agent': ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
                            '(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'),
            'Referer': 'https://easy.lagou.com/im/chat/index.htm',
            'Upgrade-Insecure-Requests': '1',
            'Accept-Language': 'zh,zh-CN;q=0.8,en;q=0.6,zh-TW;q=0.4'
        }
        self.temp_data = []  # 仅将一个页面所有文章解析信息暂存列表中
        self.temp_link = []  # 招聘信息不含eamil的文章链接

    def get_next_page(self, current_page_url):
        """输入当前url地址，获取下一页url地址"""
        text = requests.get(current_page_url, headers=self.headers).text
        tree = html.fromstring(text)
        result = tree.xpath('/html/body/form/center/nobr/a[4]/@href')
        next_url = self.prefix_url+result[0]
        return next_url

    def get_job_link(self, page_url):
        """输入网页url，反序输出该网页所有招聘信息url"""
        text = requests.get(page_url, headers=self.headers).text
        soup = BeautifulSoup(text)
        article_link = []
        job_link_pattern = re.compile(r'bbscon[?,]board[,=](JobInfo|JobForum)[,&]file')
        for link in soup.find_all('a'):
            temp = link.get('href')
            try:
                if re.search(job_link_pattern, temp).group():
                    article_link.append('https://bbs.sjtu.edu.cn/' + temp)
            except AttributeError:
                pass
        # with open('templink.txt', mode='w') as f:
        #     for e in article_link:
        #         f.write(e+'\n')
        article_link.reverse()
        return article_link

    def article_parse(self, article_link):
        """输入招聘信息url，招聘信息解析,输出邮箱 发帖时间 标题 电话形成的列表"""
        print(article_link)
        infolist = []
        time_string = ''
        title = ''
        target_article = ""
        text = requests.get(article_link, headers=self.headers).text
        target_article_list = html.fromstring(text).xpath('//pre/text()')
        for article in target_article_list:
            target_article += article
        email_pattern = re.compile(r'[a-zA-Z0-9]+[.]?[\w]+@[0-9a-zA-z-]+[.][a-zA-z]+[.]?[a-zA-Z]*[.]?[a-zA-Z]*')
        time_pattern = re.compile(r'[0-9]+')
        tel_pattern = re.compile(r'1\d{10}')
        try:
            time_string = target_article.split('\n')[2]
            title = target_article.split('\n')[1].split(':')[1].strip()
        except TypeError:
            pass
        email = ""
        tel = ""
        time_list = []
        email_time = ""
        try:
            email = re.search(email_pattern, target_article).group()
        except AttributeError:
            # print('-'*5 + "邮件格式匹配错误" + '-'*5)
            self.temp_link.append(article_link)
            pass
        try:
            tel = re.search(tel_pattern, target_article).group()
        except AttributeError:
            # print('-' * 5 + "招聘信息没有电话" + '-' * 5)
            pass
        try:
            time_list = re.findall(time_pattern, time_string)
        except AttributeError:
            # print('-' * 5 + "时间格式匹配错误" + '-' * 5)
            pass

        if len(time_list) >= 3:
            email_time = time_list[0] + '/' + time_list[1] + '/' + time_list[2] + " " + time_list[3] + ":" + time_list[4]
        if email != "":
            infolist.append(email)
            infolist.append(email_time)
            infolist.append(title)
            infolist.append(tel)
        if infolist:
            self.temp_data.append(infolist)
            return 1
        return 0

    def clear_same_title(self):
        """
        将一个页面中相同邮箱的帖子中，除去旧帖子，只保留最新的一个
        :return:
        """
        title_list = []
        index_list = []
        for post in self.temp_data:
            title_list.append(post[2])
        for i in range(0, len(title_list)):
            if title_list.index(title_list[i]) != i:
                index_list.append(i)
        index_list.reverse()
        if index_list:
            for n in index_list:
                del self.temp_data[n]
        return

    def data_entry(self, text):
        """爬取信息self.temp_data录入到text中"""
        # print(self.temp_data)
        with open(text[0], mode='a') as f:
            for tem in self.temp_data:
                f.write(str(tem) + '\n')
        with open(text[1], mode='a') as f:
            for tem in self.temp_link:
                f.write(str(tem) + '\n')
        return

    @staticmethod
    def new_file():
        """新建数据存储文件"""
        t_human = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        data_path = os.path.join(os.path.dirname(__file__), 'data/{}/'.format(t_human))
        if not os.path.exists(data_path):
            os.makedirs(data_path)
        data_file = os.path.join(data_path, 'data.txt')
        no_email_link = os.path.join(data_path, 'no_email_link.txt')
        return data_file, no_email_link

    def crawl(self, page_url, file, page_num=10):
        """爬虫程序！
           page_url:爬取页面地址
           file：数据存储文件
           page_num:最大爬去页面数"""
        total_job_link = 0
        success_link = 0
        for i in range(0, page_num):
            job_link = self.get_job_link(page_url)
            total_job_link += len(job_link)
            for link in job_link:
                success_link += self.article_parse(link)
            page_url = self.get_next_page(page_url)
            self.clear_same_title()
            self.data_entry(file)
            self.temp_data = []
            self.temp_link = []
        print('招聘信息总数：' + str(total_job_link))
        print('含有邮箱的招聘信息数目：' + str(success_link))
        if total_job_link:
            success = success_link / total_job_link
        else:
            success = 0
        print('成功率：%.2f%%  :)' % (success * 100))
        return


def main():
    search = JobSearch()
    choice = input("请输入要爬取的BBS：就业信息（1） or 求职交流（2） \n")
    num = input("请输入要爬取的页数(默认5页）：\n")
    if int(num) <= 0 or not num.isdigit():
        print("对不起，您要求爬取的页数不符合要求！系统将默认爬取5页数据")
        num = 5
    else:
        num = int(num)

    if choice == "就业信息" or int(choice) == 1:
        print("*****就业信息正在爬取*****")
        search.base_url = "https://bbs.sjtu.edu.cn/bbsdoc?board=JobInfo"
    elif choice == "求职交流" or int(choice) == 2:
        print("*****求职交流正在爬取*****")
        search.base_url = "https://bbs.sjtu.edu.cn/bbsdoc?board=JobForum"
    else:
        print("请选择1 or 2")
        return
    search.crawl(search.base_url, search.new_file(), page_num=num)


if __name__ == '__main__':
    main()
