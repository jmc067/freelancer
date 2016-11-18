import os
from pymongo import MongoClient

_mongodb = None

## Connects to Mongo.  Single global mongodb connection 
def connect_mongo():
	global _mongodb
	if not _mongodb:
		if "MONGO_URI" in os.environ:
			mongo_uri = os.environ['MONGO_URI']
		else:
			mongo_uri = "mongodb://localhost:27017/"

		client = MongoClient()
		if client==None:
			raise ValueError('Error Connecting to Mongo')
		else: 
			print "Connected to Mongo..."
			_mongodb = client.local
			return _mongodb
	else:
		return _mongodb

def insert(doc,collection):
	return _mongodb[collection].insert(doc)
