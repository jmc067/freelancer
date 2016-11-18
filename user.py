from mongo import *
from constants import *
from errors import *
from inbox import *
from ledger import *
from dict_helpers import *
import scrambler

# Public Functions
def create_user(user_params):
	user = copy(user_params)
	validate_signup_fields(user)
	validate_role(user)
	setup_inbox(user) # TODO add error handling
	setup_ledger(user)  # TODO add error handling
	salt_password(user)
	clean(user)
	validate_all_required_fields(user)
	return insert_user(user) # TODO add error handling

def get_users():
	return get_user({}) # TODO add error handling

# User Validation
def validate_signup_fields(user_params):
	for user_param in USER_SIGNUP_FIELDS:
		if user_param not in user_params:
			error_bad_request("Missing Field: " + user_param)	

def validate_all_required_fields(user_params):
	for user_param in REQUIRED_USER_FIELDS:
		if user_param not in user_params:
			error_bad_request("Missing Field: " + user_param)	

def validate_role(user_params):
	role = user_params["role"]
	if role not in SUPPORTED_ROLES:
		error_bad_request("Unsupported Role")	

# Formatting
def salt_password(user):
	if field=="salted_password":
		user["salted_password"] = scrambler.hash(user["password"])	
		user.pop("password")

def clean(user): 
	for field in SUPPORTED_USER_FIELDS:
		print field, str(user[field])
		if field=="_id" or field=="inbox_id" or field=="ledger_id":
			user[field] = str(user[field])
	return user

# Mongo Funcitons
def insert_user(user):
	return insert(user,"users")	

def get_user(query):
	return list(get(query,"users"))

def update(query,update,options,collection):
	return update(query,update,options,collection)
