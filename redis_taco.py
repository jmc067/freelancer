from redis import Redis
from constants import *

_redis = None

## Connects to Local Redis.  Single global redis connection 
# TODO fix the connection check.  False positives
def connect():
	global _redis
	if not _redis:
		# Get Redis Client
		_redis = Redis(
			host='redis', 
			port=6379
		)
		if _redis==None:
			raise ValueError('Error connecting to Redis')		
		else: 
			print "Connected to Redis..."
			return _redis
	else:
		return _redis

# TODO error handling if set didnt work
def set(key,value):
	return _redis.set(str(key), str(value))

def expire(key,ttl):
	return _redis.expire(str(key), ttl)

def get(key):
	return _redis.get(str(key))

def delete(key):
	return _redis.delete(str(key))

def geoadd(key,lon,lat,radius,member,with_distance=True):
	return _redis.geoadd(key,lon,lat,member,radius,"mi",with_distance)
