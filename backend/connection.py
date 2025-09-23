from pymongo import MongoClient
from os import environ

MONGO_URL = environ.get('MONGO_URL', 'mongodb://localhost:27017/gehenna')

client = MongoClient(MONGO_URL)

db = client['gehenna']

coll = db['names']
