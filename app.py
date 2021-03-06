from flask import Flask
from flask import request
import os
import mongo_burrito
import redis_taco
import tracker
import postman
from user import *
from category import *
from subcategory import *
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

# READ, UPDATE, DELETE user
@app.route('/user/<user_id>', methods = ['GET', 'POST', 'DELETE'])
def user_actions(user_id):

	# READ
	if request.method == 'GET':
		validate_bson(user_id)
		user = [ clean_dict(user) for user in get_users({"_id":to_bson(user_id)}) ]
		return to_json(user)

	# UPDATE  # TODO add better response
	if request.method == 'POST':
		validate_bson(user_id)
		user_id = edit_user(user_id,request.values)
		return to_json(str(True))

	# DELETE # TODO add better response
	if request.method == 'DELETE':
		validate_bson(user_id)
		delete_user(user_id)
		return to_json(str(True))

# GET users
@app.route('/user/search', methods = ['GET'])
def list_users():
	users = [ clean_dict(user) for user in search_users(request.values) ]
	return to_json(users)

####################################
### Auth Routes
####################################

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


####################################
### Category Routes
####################################

# CREATE category
@app.route('/category/create', methods = ['POST'])
def new_category():
	category = create_category(request.values)
	return to_json(category)

# READ, UPDATE, DELETE category
@app.route('/category/<category_id>', methods = ['GET', 'POST', 'DELETE'])
def category_actions(category_id):

	# READ
	if request.method == 'GET':
		validate_bson(category_id)
		category = [ clean_dict(category) for category in get_categories({"_id":to_bson(category_id)}) ]
		return to_json(category)

	# UPDATE  TODO add better response
	if request.method == 'POST':
		validate_bson(category_id)
		category_id = edit_category(category_id,request.values)
		return to_json(str(True))

	# DELETE  TODO add better response
	if request.method == 'DELETE':
		validate_bson(category_id)
		delete_category_tree(category_id)
		return to_json(str(True))

# GET categories
@app.route('/category/search', methods = ['GET'])
def list_categories():
	categories = [ clean_dict(category) for category in search_categories(request.values) ]
	return to_json(categories)


####################################
### Subategory Routes
####################################

# CREATE subcategory
@app.route('/subcategory/create', methods = ['POST'])
def new_subcategory():
	subcategory = create_subcategory(request.values)
	return to_json(subcategory)

# READ, UPDATE, DELETE subcategory
@app.route('/subcategory/<subcategory_id>', methods = ['GET', 'POST', 'DELETE'])
def subcategory_actions(subcategory_id):

	# READ
	if request.method == 'GET':
		validate_bson(subcategory_id)
		subcategory = [ clean_dict(subcategory) for subcategory in get_subcategories({"_id":to_bson(subcategory_id)}) ]
		return to_json(subcategory)

	# UPDATE  TODO add better response
	if request.method == 'POST':
		validate_bson(subcategory_id)
		subcategory_id = edit_subcategory(subcategory_id,request.values)
		return to_json(str(True))

	# DELETE  TODO add better response
	if request.method == 'DELETE':
		validate_bson(subcategory_id)
		delete_subcategory(subcategory_id)
		return to_json(str(True))

# GET categories
@app.route('/subcategory/search', methods = ['GET'])
def list_subcategories():
	subcategories = [ clean_dict(subcategory) for subcategory in search_subcategories(request.values) ]
	return to_json(subcategories)


####################################
### Location Routes
####################################

# POST Track users location
@app.route('/location', methods = ['POST','GET'])
def location():
	# Store by location
	if request.method == 'POST':
		return to_json(tracker.track(request.values))

	# Query by location.  Returns active WORKER users only
	if request.method == 'GET':
		users = [ clean_dict(user) for user in tracker.search(request.values) ]
		return to_json(users)

####################################
### Messager Routes
####################################

@app.route('/postman/<recipient_user_id>', methods = ['POST'])
def deliver(recipient_user_id):
	postman.deliver(recipient_user_id,request.values)
	return "True" # TODO better response

@app.route('/postman', methods = ['GET'])
def get_mail():
	inbox = postman.get_inbox(request.values)
	return "True" # TODO better response


# SERVER START UP
if __name__ == "__main__":
	if "DEBUG" in os.environ:
		print "Entering Debug Mode..."
		debug = True
	else:
		debug = False
	app.run(host='0.0.0.0',debug=debug,port=5000)
