import bson.objectid
from errors import *
from constants import *

def validate_bson(id):
	if not bson.objectid.ObjectId.is_valid(str(id)):
		error_bad_request("Invalid BSON ID")

def to_bson(string):
	return bson.ObjectId(str(string))

# converts all BSON Object ids into strings
def clean_dict(dictionary):
	for field in dictionary:
		if field in BSON_FIELDS:
			dictionary[field] = str(dictionary[field])
	return dictionary

