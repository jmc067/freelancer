import mongo_burrito
import redis_taco
from constants import *
from errors import *
from inbox import *
from ledger import *
from dict_helpers import *
from jsonify import *
from bsonify import *
from category import *
from subcategory import *
import scrambler
# TODO refactor out auth/session into seperate file
# TODO refactor to use Python Classes

# Public Functions
def create_user(user_params):
	user = copy(user_params)
	ensure_signup_fields(user)
	check_email_availability(user["email"])
	validate_role(user)
	validate_categories(user)
	validate_subcategories(user)
	setup_inbox(user) # TODO add error handling
	setup_ledger(user)  # TODO add error handling
	salt_password(user)
	user = format_user(user)
	user.update({"_id":str(insert_user(user))}) # TODO add error handling
	return format_user_response(user)

def edit_user(user_id, user_params):
	user_updates = copy_editable_user_fields(user_params)
	if "email" in user_updates:
		check_email_availability(user_updates["email"])
	if "categories" in user_updates:
		validate_categories(user_updates)
	if "subcategories" in user_updates:
		validate_subcategories(user_updates)
	user_updates = format_user(user_updates)
	return update_user(user_id,user_updates) # TODO add error handling.  Have a been response than mongo output

def search_users(params):
	query = {}
	for param in params:
		if param in SUPPORTED_USER_FIELDS:   # you can search for any supported field on user doc
			query[param] = params[param]
	return get_users(query)	

def authorize(params):
	ensure_authentication_fields(params)
	user = ensure_user(params["email"])
	validate_password(params["password"],user["salted_password"])
	return activate_session(user)

def deactivate_session(params):
	ensure_scramble(params)
	expire_session(params["scramble"])	
	return True

def extend_session(params):
	ensure_scramble(params)
	extend_expiration(params["scramble"])	
	return True

def check_authorization(params):
	ensure_scramble(params)
	ensure_session(params["scramble"])	

# User Validation
def ensure_authentication_fields(params):
	for field in AUTHENTICATION_FIELDS:
		if field not in params:
			error_bad_request("Insufficient Authentication fields")

def ensure_user(email):
	users = get_users({"email":email})
	if len(users)==0:
		error_bad_request("No account registered with this email")
	elif len(users)==1:
		return users[0]
	else:
		error_bad_request("Oh no!  It seems that there are multiple accounts associated with this email.\nFor your security, you must contact an administrator before continuing")

def validate_password(password,salted_password):
	if not scrambler.is_match(password,salted_password): 
		error_forbidden("Incorrect Email or Password")

def ensure_scramble(params):
	if "scramble" not in params:
		error_bad_request("No scramble token provided") 

# TODO make sure user matches scramble?
#  add ttl for session expiration
def ensure_session(scramble):
	user_id = redis_taco.get(scramble)
	if user_id==None:
		error_forbidden("No session found")
	else:
		return True

def expire_session(scramble):
	redis_taco.delete(scramble)

def extend_expiration(scramble):
	redis_taco.expire(scramble,SESSION_LENGTH)
	return True

def activate_session(user):
	scramble = scrambler.scramble()
	redis_taco.set(scramble,str(user["_id"]))
	redis_taco.expire(scramble,SESSION_LENGTH)
	return scramble

def ensure_signup_fields(user_params):
	for user_param in SIGNUP_USER_FIELDS:
		if user_param not in user_params:
			error_bad_request("Missing Field: " + user_param)	

def check_email_availability(email):
	users = get_users({"email":email})
	if len(users) > 0:
		error_bad_request("Account already registered with this email")	

def format_user_response(user):
	formatted_user_response = {}
	for user_param in SUPPORTED_USER_FIELDS :
		if user_param not in SENSITIVE_USER_FIELDS:
			if user_param in user:
				formatted_user_response[user_param] = user[user_param]
	return formatted_user_response

def copy_editable_user_fields(user_params):
	editable_fields = {}
	for field in user_params:
		if field in EDITABLE_USER_FIELDS:
			editable_fields[field] = user_params[field]
	return editable_fields

def validate_categories(user):
	if "categories" in user:
		for category_id in [category.strip() for category in user["categories"].split(',')]:
			validate_bson(category_id)
			if not get_categories({"_id":to_bson(category_id)}):
				error_bad_request("Category not found")

def validate_subcategories(user):
	if "subcategories" in user:
		for subcategory_id in [subcategory.strip() for subcategory in user["subcategories"].split(',')]:
			validate_bson(subcategory_id)
			if not get_subcategories({"_id":to_bson(subcategory_id)}):
				error_bad_request("Subcategory not found")

# todo make sure they have proper permissions in order to validate
def validate_role(user_params):
	role = user_params["role"]
	if role not in SUPPORTED_USER_ROLES:
		error_bad_request("Unsupported Role")	

# Formatting
def salt_password(user):
	user["salted_password"] = scrambler.hash(user["password"])	
	user.pop("password")

def format_user(user):
	formatted_user = {}
	for field in SUPPORTED_USER_FIELDS:
		if field in user:
			# convert categories && subcategories to arrays
			if field=="categories" or field=="subcategories":
				formatted_user[field] = [x.strip() for x in user[field].split(',')]
			else:
				formatted_user[field] = user[field]
	return formatted_user

# Mongo Funcitons
def insert_user(user):
	return mongo_burrito.insert(user,"users")	

def get_users(query):
	return list(mongo_burrito.get(query,"users"))

def update_user(user_id,user_updates):
	return mongo_burrito.update({"_id":to_bson(user_id)},{"$set":user_updates},False,"users")

def delete_user(user_id):
	return mongo_burrito.delete({"_id":to_bson(user_id)},"users") 
