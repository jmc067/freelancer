from flask import Flask
from flask import request
import os
import mongo_burrito
import redis_taco
from user import *
from errors import *
from jsonify import *
from bsonify import *
from constants import *

app = Flask(__name__)

####################################
### Establish Database Connections
####################################
mongo_burrito.connect() 
redis_taco.connect()

####################################
### Welcome Message
####################################
@app.route("/")
def welcome():
    return "Welcome to freelancer!"

@app.before_request
def before_request():
	if request.path not in PUBLIC_ROUTES:
		check_authorization(request.values)
		extend_session(request.values)

####################################
### User Routes
####################################
# CREATE user
@app.route('/user/signup', methods = ['POST'])
def signup():
	user = create_user(request.values)
	return to_json(clean_dict(user))

@app.route('/user/login', methods = ['POST'])
def login():
	scramble_token = authorize(request.values)
	return to_json(str(scramble_token))

@app.route('/user/logout', methods = ['POST'])
def logout():
	deactivated = deactivate_session(request.values)
	return to_json(str(deactivated))

@app.route('/user/extend_session', methods = ['POST'])
def extend():
	extended = extend_session(request.values)
	return to_json(str(extended))


# READ, UPDATE, DELETE user
@app.route('/user/<user_id>', methods = ['GET', 'POST', 'DELETE'])
def user_actions(user_id):

	# READ
	if request.method == 'GET':
		validate_bson(user_id)
		user = [ clean_dict(user) for user in get_users({"_id":to_bson(user_id)}) ]
		return to_json(user)

	# UPDATE
	if request.method == 'POST':
		validate_bson(user_id)
		user_id = edit_user(user_id,request.values)
		return to_json(str(True))

	# DELETE
	if request.method == 'DELETE':
		validate_bson(user_id)
		return to_json(str(True))

# GET users
@app.route('/user/search', methods = ['GET'])
def list_users():
	users = [ clean_dict(user) for user in search_users(request.values) ]
	return to_json(users)



####################################
### Category Routes
####################################

# CREATE user
@app.route('/category/new', methods = ['POST'])
def new_category():
	category = create_category(request.values)
	return to_json(category)


# SERVER START UP
if __name__ == "__main__":
	if "DEBUG" in os.environ:
		print "Entering Debug Mode..."
		debug = True
	else:
		debug = False

	app.run(debug=debug)