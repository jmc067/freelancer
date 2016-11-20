import mongo_burrito
import dict_helpers
from category import *
from constants import * 
from errors import * 
from bsonify import * 

def create_subcategory(subcategory_params):
	subcategory = dict_helpers.copy(subcategory_params)
	ensure_create_subcategory_fields(subcategory)
	check_parent_category_validity(subcategory["parent_category"])
	check_subcategory_availability(subcategory)
	subcategory = format_subcategory(subcategory)
	subcategory.update({"_id":str(insert_subcategory(subcategory))}) # TODO add error handling
	return format_subcategory_response(subcategory)

def edit_subcategory(subcategory_id, subcategory_params):
	subcategory_updates = copy_editable_subcategory_fields(subcategory_params)
	if subcategory_updates:
		if "parent_category" in subcategory_updates:
			check_parent_category_validity(subcategory_updates["parent_category"])
		return update_subcategory(subcategory_id,subcategory_updates) # TODO add error handling.  Have a been response than mongo output

def search_subcategories(params):
	query = {}
	for param in params:
		if param in SUPPORTED_SUBCATEGORY_FIELDS:   # you can search for any supported field on subcategory doc
			query[param] = params[param]
	return get_subcategories(query)	

# TODO add error handling
def delete_subcategory_tree(subcategory_id):
	delete_subcategory(subcategory_id)	
	delete_subsubcategories(subcategory_id)	
	return True

def check_parent_category_validity(parent_category_id):
	validate_bson(parent_category_id)
	categories = get_categories({"_id":to_bson(parent_category_id)})
	if not categories:
		error_bad_request("Parent category not found")

def check_subcategory_availability(subcategory_params):
	subcategories = get_subcategories({"name":subcategory_params["name"],"parent_category":subcategory_params["parent_category"]})	
	if subcategories:
		error_bad_request("Subcategory already exists")

def ensure_create_subcategory_fields(subcategory_params):
	for subcategory_param in CREATE_SUBCATEGORY_FIELDS:
		if subcategory_param not in subcategory_params:
			error_bad_request("Missing Field: " + subcategory_param)	

def copy_editable_subcategory_fields(subcategory_params):
	editable_fields = {}
	for field in subcategory_params:
		if field in EDITABLE_SUBCATEGORY_FIELDS:
			editable_fields[field] = subcategory_params[field]
	return editable_fields

def format_subcategory(subcategory):
	formatted_subcategory = {}
	for field in SUPPORTED_SUBCATEGORY_FIELDS:
		if field in subcategory:
			formatted_subcategory[field] = subcategory[field]
	return formatted_subcategory

def format_subcategory_response(subcategory):
	return subcategory

# Mongo Funcitons
def insert_subcategory(subcategory):
	return mongo_burrito.insert(subcategory,"subcategories")

def get_subcategories(query):
	return list(mongo_burrito.get(query,"subcategories"))

def update_subcategory(subcategory_id,subcategory_updates):
	return mongo_burrito.update({"_id":to_bson(subcategory_id)},{"$set":subcategory_updates},False,"subcategories")

def delete_subcategory(subcategory_id):
	return mongo_burrito.delete({"_id":to_bson(subcategory_id)},"subcategories") 

