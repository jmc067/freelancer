import mongo_burrito
import dict_helpers
import redis_taco
from constants import * 
from errors import * 
from bsonify import * 

def track(params):
	dict_helpers.pretty_print(params)
	validate_location_search_params(params)
	store_location(params["lat"],params["lon"],params["scramble"],params["radius"])	

def validate_location_search_params(params):
	ensure_lat(params)
	ensure_lon(params)
	ensure_radius(params)

def ensure_lat(params):
	if "lat" not in params:
		error_bad_request("No latitude position specified")

def ensure_lon(params):
	if "lon" not in params:
		error_bad_request("No longitude position specified")

def ensure_radius(params):
	if "radius" not in params:
		error_bad_request("No radius specified")

def store_location(lon,lat,member,radius):
	redis_taco.geoadd("tracker",lon,lat,member,radius)

