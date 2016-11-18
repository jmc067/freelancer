import os
from pymongo import MongoClient

_mongodb = None

## Connects to Local Mongo.  Single global mongodb connection 
def connect_mongo():
	global _mongodb
	if not _mongodb:
		# Get Mongo Client
		ON_COMPOSE = os.environ.get('COMPOSE')
		if ON_COMPOSE:
			mongo_client = MongoClient(os.environ['DB_PORT_27017_TCP_ADDR'],27017)
		else:
			mongo_client = MongoClient('mongodb://localhost:27017/')	

		_mongodb = mongo_client.local
		print "Connected to Mongo..."
		return _mongodb
	else:
		return _mongodb

def insert(doc,collection):
	return _mongodb[collection].insert(doc)

def get(query,collection):
	return _mongodb[collection].find(query)

def update(query,update,options,collection):
	return _mongodb[collection].update(query,update,options)

def delete(query,collection):
	return _mongodb[collection].remove(query)
