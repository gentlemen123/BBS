from pymongo import MongoClient

db = MongoClient().get_database('beijingwaiguoyu')
col = db.get_collection('articles')

col.update({'status': 'done'}, {'$set': {'status': 'not_done'}}, multi=True)
