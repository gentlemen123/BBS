# from pymongo import MongoClient
#
# db = MongoClient().get_database('beijingwaiguoyu')
# col = db.get_collection('articles')
#
# col.update({'status': 'done'}, {'$set': {'status': 'not_done'}}, multi=True)

import requests

resp = requests.get("http://www.xgbbs.net/xgbbs/dispbbs.asp?boardid=56&Id=1360383&page=2")
with open('index.html' ,"a+") as f:
    f.write(resp.text)