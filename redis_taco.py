from redis import Redis

_redis = None

## Connects to Local Redis.  Single global redis connection 
# TODO fix the connection check.  False positives
def connect():
	global _redis
	if not _redis:
		# Get Redis Client
		_redis = Redis(
			host='127.0.0.1', 
			port=6379
		)
		print _redis
		_redis.set("test","true")
		if _redis==None:
			raise ValueError('Error connecting to Redis')		
		else:
			print "Connected to Redis..."
			return _redis
	else:
		return _redis

def set(key,value):
	_redis.set(str(key), str(value))

def get(key):
	_redis.get(str(key))




