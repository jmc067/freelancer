import mongo_burrito
import dict_helpers
from constants import * 
from errors import * 

def create_category(category_params):
	category = dict_helpers.copy(category_params)
	ensure_create_category_fields(category)
	category = format_category(category)
	category.update({"_id":str(insert_category(category))}) # TODO add error handling
	return format_category_response(category)

# def create_subcategory(subcategory_params):
def ensure_create_category_fields(category_params):
	for category_param in CREATE_CATEGORY_FIELDS:
		if category_param not in category_params:
			error_bad_request("Missing Field: " + category_param)	

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
