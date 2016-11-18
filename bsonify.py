import bson.objectid
from errors import *

def validate_bson(id):
	if not bson.objectid.ObjectId.is_valid(str(id)):
		error_bad_request("Invalid User Id")

def to_bson(string):
	return bson.ObjectId(str(string))
