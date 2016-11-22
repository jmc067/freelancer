import datetime
from errors import *
from user import *
from bsonify import *

def deliver(recipient_user_id,params):
	validate_bson(recipient_user_id)
	ensure_message(params)
	record_message(recipient_user_id,params)		

def ensure_message(params):
	if "message" not in params:
		error_bad_request("No message specified")

def record_message(recipient_user_id,params):
	# get sender user_id
	sender_user_id = redis_taco.get(params["scramble"])

	# Format message
	message = {
		"message":params["message"],
		"timestamp":datetime.datetime.now(),
		"from":str(sender_user_id),
		"to":str(recipient_user_id)
	}

	# store on sender inbox
	send_to_inbox(sender_user_id,message)

	# store on recipient inbox
	send_to_inbox(recipient_user_id,message)

def send_to_inbox(user_id,message):	
	# get user
	users = get_users({"_id":to_bson(user_id)})
	if users:
		user = users[0]
		inbox = user["inbox"]

		# create/update conversation with recipient
		if user_id in inbox:
			inbox[user_id].append(message)
		else:
			inbox[user_id] = [message]	
		update_user(user_id,user)	
	else:
		error_bad_request("User not found")	
