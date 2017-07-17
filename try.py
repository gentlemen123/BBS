import requests


headers = {
        'Pragma': 'no-cache',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/57.0.2987.133 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Referer': 'http://bbs.cloud.icybee.cn/board/JobInfo',
        'Connection': 'keep-alive',
        'Cache-Control': 'no-cache',
    }
response = requests.get("http://www.xgbbs.net/xgbbs/index.asp?boardid=56&TopicMode=0&List_Type=&Page=1", headers=headers)

with open('index.html', mode='w+') as f:
    f.write(response.text)