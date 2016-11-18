from mongo import *
from constants import *
from errors import *
from inbox import *
from ledger import *
import scrambler

def create_user(user_params):
	user = copy(user_params)
	validate_signup_fields(user)
	validate_role(user)
	setup_inbox(user) # add error handling
	setup_ledger(user)  # add error handling
	clean(user)
	validate_all_required_fields(user)
	return insert_user(user) # add error handling

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

def copy(user_params):
	user = {}
	for user_param in user_params:
		user[user_param] = user_params[user_param]
	return user

def clean(user): 
	for field in SUPPORTED_USER_FIELDS:
		if field=="salted_password":
			user["salted_password"] = scrambler.hash(user["password"])	
			user.pop("password")
		if field=="_id" or field=="inbox_id" or field=="ledger_id":
			user[field] = str(user[field])
	return user

def insert_user(user):
	return insert(user,"users")	
