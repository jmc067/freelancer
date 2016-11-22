import redis
from constants import *

_redis = None

## Connects to Local Redis.  Single global redis connection 
# TODO fix the connection check.  False positives
def connect():
	global _redis
	if not _redis:
		# Get Redis Client
		_redis = redis.StrictRedis(
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

def geoadd(lon,lat,member):
	return _redis.execute_command("geoadd","geo_tracker",lon,lat,member)

def georadius(lon,lat,radius):
	return _redis.execute_command("georadius","geo_tracker",lon,lat,radius,"mi","WITHDIST")
