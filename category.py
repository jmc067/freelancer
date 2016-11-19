import mongo_burrito
import dict_helpers
from constants import * 
from errors import * 
from bsonify import * 

def create_category(category_params):
	category = dict_helpers.copy(category_params)
	ensure_create_category_fields(category)
	category = format_category(category)
	category.update({"_id":str(insert_category(category))}) # TODO add error handling
	return format_category_response(category)

def edit_category(category_id, category_params):
	category_updates = copy_editable_category_fields(category_params)
	if category_updates:
		return update_category(category_id,category_updates) # TODO add error handling.  Have a been response than mongo output

def search_categories(params):
	query = {}
	for param in params:
		if param in SUPPORTED_CATEGORY_FIELDS:   # you can search for any supported field on category doc
			query[param] = params[param]
	return get_categories(query)	


def ensure_create_category_fields(category_params):
	for category_param in CREATE_CATEGORY_FIELDS:
		if category_param not in category_params:
			error_bad_request("Missing Field: " + category_param)	

def copy_editable_category_fields(category_params):
	editable_fields = {}
	for field in category_params:
		if field in EDITABLE_CATEGORY_FIELDS:
			editable_fields[field] = category_params[field]
	return editable_fields

def format_category(category):
	formatted_category = {}
	for field in SUPPORTED_CATEGORY_FIELDS:
		if field in category:
			formatted_category[field] = category[field]
	return formatted_category

def format_category_response(category):
	return category

# Mongo Funcitons
def insert_category(category):
	return mongo_burrito.insert(category,"categories")

def get_categories(query):
	return list(mongo_burrito.get(query,"categories"))

def update_category(category_id,category_updates):
	return mongo_burrito.update({"_id":to_bson(category_id)},{"$set":category_updates},False,"categories")

def delete_category(category_id):
	return mongo_burrito.delete({"_id":to_bson(category_id)},"categories") 
