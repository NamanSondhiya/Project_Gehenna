from pymongo import MongoClient
from os import environ

MONGO_URL = environ.get('MONGO_URL', 'localhost')

client = MongoClient(MONGO_URL, 27017)

db = client['gehenna']

coll = db['names']
