import mongo_burrito
import redis_taco
from constants import *
from errors import *
from inbox import *
from ledger import *
from dict_helpers import *
from bsonify import *
import scrambler
# TODO refactor out auth/session into seperate file
# TODO refactor to use Python Classes

# Public Functions
# TODO make sure email isn't already in use
def create_user(user_params):
	user = copy(user_params)
	ensure_signup_fields(user)
	validate_role(user)
	setup_inbox(user) # TODO add error handling
	setup_ledger(user)  # TODO add error handling
	salt_password(user)
	format_user(user)
	user.update({"_id":str(insert_user(user))}) # TODO add error handling
	return format_user_response(user)

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
	return activate_session(user["_id"])

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

def edit_user(user_id, user_params):
	user_updates = copy_editable_fields(user_params)
	return update_user(user_id,user_updates) # TODO add error handling.  Have a been response than mongo output

# User Validation
def ensure_authentication_fields(params):
	for field in AUTHENTICATION_FIELDS:
		if field not in params:
			error_bad_request("Insufficient Authentication fields")

def ensure_user(email):
	users = get_users({"email":email})
	print users
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
	print user_id
	if user_id==None:
		error_forbidden("No session found")
	else:
		return True

def expire_session(scramble):
	redis_taco.delete(scramble)

def extend_expiration(scramble):
	redis_taco.expire(scramble,SESSION_LENGTH)
	return True

def activate_session(user_id):
	scramble = scrambler.scramble()
	redis_taco.set(scramble,user_id)
	redis_taco.expire(scramble,SESSION_LENGTH)
	return scramble

def ensure_signup_fields(user_params):
	for user_param in SIGNUP_USER_FIELDS:
		if user_param not in user_params:
			error_bad_request("Missing Field: " + user_param)	

def format_user_response(user):
	formatted_user_response = {}
	for user_param in SUPPORTED_USER_FIELDS :
		if user_param not in SENSITIVE_USER_FIELDS:
			if user_param in user:
				formatted_user_response[user_param] = user[user_param]
	return formatted_user_response

def copy_editable_fields(user_params):
	editable_fields = {}
	for field in user_params:
		if field in EDITABLE_USER_FIELDS:
			editable_fields[field] = user_params[field]
	return editable_fields

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
	for field in SUPPORTED_USER_FIELDS:
		if field in user:
			user[field] = user[field]

# Mongo Funcitons
def insert_user(user):
	return mongo_burrito.insert(user,"users")	

def get_users(query):
	return list(mongo_burrito.get(query,"users"))

def update_user(user_id,user_updates):
	return mongo_burrito.update({"_id":to_bson(user_id)},{"$set":user_updates},False,"users")

def delete_user(user_id):
	return mongo_burrito.delete({"_id":to_bson(user_id)},"users") 
