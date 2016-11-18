from flask import Flask
from flask import request
import os
from mongo import connect_mongo
from user import *
from errors import *
from jsonify import *
from bsonify import *

app = Flask(__name__)

####################################
### Establish Mongo Connection
####################################
connect_mongo() 

####################################
### Welcome Message
####################################
@app.route("/")
def welcome():
    return "Welcome to freelancer!"

####################################
### User Routes
####################################
# CREATE user
@app.route('/signup', methods = ['POST'])
def signup():
	user_id = create_user(request.values)
	return to_json(str(user_id))

# READ, UPDATE, DELETE user
@app.route('/user/<user_id>', methods = ['GET', 'POST', 'DELETE'])
def user_actions(user_id):

	# READ
	if request.method == 'GET':
		validate_bson(user_id)
		user = [ clean(user) for user in get_users({"_id":to_bson(user_id)}) ]
		return to_json(user)

	# UPDATE
	if request.method == 'POST':
		validate_bson(user_id)
		user_id = edit_user(user_id,request.values)
		print user_id
		return "true"

	# DELETE
	if request.method == 'DELETE':
		validate_bson(user_id)
		return str(delete_user(user_id))

# GET users
@app.route('/users', methods = ['GET'])
def list_users():
	users = [ clean(user) for user in get_users({}) ]
	return to_json(users)



# SERVER START UP
if __name__ == "__main__":
	if "DEBUG" in os.environ:
		print "Entering Debug Mode..."
		debug = True
	else:
		debug = False

	app.run(debug=debug)