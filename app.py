from flask import Flask
from flask import request
from flask import abort
import os
app = Flask(__name__)

####################################
### Constants
####################################
REQUIRED_USER_FIELDS = ["first_name","last_name","role","email","salted_password","token","inbox_id","jobs_id"]
SUPPORTED_ROLES = ["CLIENT","WORKER","ADMIN"]

@app.route("/")
def hello():
    return "Welcome to freelancer!"

####################################
### Account Management Routes
####################################
# CREATE user
@app.route('/user', methods = ['POST'])
def create_user():
	check_user_fields(request.values)
	return store_user("user")

# READ, UPDATE, DELETE user
@app.route('/user/<user_id>', methods = ['GET', 'POST', 'DELETE'])
def user(user_id):

	# READ
	if request.method == 'GET':
		return "READ user by id"

	# UPDATE
	if request.method == 'POST':
		return "UPDATE user by id"

	# DELETE
	if request.method == 'DELETE':
		return "DELETE user by id"

# GET users
@app.route('/users', methods = ['GET'])
def user(user_id):
	return "GET all users"



####################################
### Helper Functions
####################################
# Store User
def store_user(user):
	return user

# Validate user values
def check_user_fields(user_fields):
	for user_field in REQUIRED_USER_FIELDS:
		# Ensure Required fields are all present
		if user_field in user_fields:
			# Validate user role
			if user_field=="role":
				if user_fields[user_field] not in SUPPORTED_ROLES:
					error_bad_request("Unsupported Role")	
		else:
			message = "Missing Field: " + user_field 
			error_bad_request(message)	

	return True

def error_bad_request(message):
	abort(400,format_message(message))

def format_message(string):
	return {'message': string}

# SERVER START UP
if __name__ == "__main__":
	if "DEBUG" in os.environ:
		print "Entering Debug Mode..."
		debug = True
	else:
		debug = False

	app.run(debug=debug)