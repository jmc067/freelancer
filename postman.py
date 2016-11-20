from errors import *
from user import *
from bsonify import *

def deliver(user_id,params):
	validate_bson(user_id)
	ensure_message(params)
	send_message(user_id,params["message"])		

def ensure_message(params):
	if "message" not in params:
		error_bad_request("No message specified")

def send_message(user_id,message):
	user = get_user({"_id":to_bson(user_id)})
	inbox = get_inbox({"_id":to_bson(user["inbox_id"])})
	inbox["messages"].append(message)

