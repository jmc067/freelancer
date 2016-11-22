import mongo_burrito
import dict_helpers
import redis_taco
from user import * 
from constants import * 
from errors import * 
from bsonify import * 

def track(params):
	validate_track_params(params)
	store_location(params["lon"],params["lat"],params["scramble"])	

def search(params):
	validate_search_params(params)
	return search_location(params["lon"],params["lat"],params["radius"])	

def validate_search_params(params):
	ensure_lon(params)
	ensure_lat(params)
	ensure_radius(params)

def validate_track_params(params):
	ensure_lon(params)
	ensure_lat(params)
	
def store_location(lon,lat,member):
	return redis_taco.geoadd(lon,lat,member)

def search_location(lon,lat,radius):
	geo_response = redis_taco.georadius(lon,lat,radius)
	geo_users = []
	for geo in geo_response:
		user_scramble = geo[0] # scramble is the first member of the geo response
		user_distance = geo[1] # distance is the second member of the geo response

		# get user_id using scramble
		user_id = redis_taco.get(user_scramble)

		# if scrambe found (aka if user is currently active)
		if user_id:

			# get user using user_ids
			users = get_users({"_id":to_bson(user_id)})

			# if user found
			if users:	
				user = users[0]
				user.update({
					"user_distance": user_distance
				})
				if user["role"]=="WORKER":
					geo_users.append(user)
	return geo_users

def ensure_lat(params):
	if "lat" not in params:
		error_bad_request("No latitude position specified")

def ensure_lon(params):
	if "lon" not in params:
		error_bad_request("No longitude position specified")

def ensure_radius(params):
	if "radius" not in params:
		error_bad_request("No radius specified")
