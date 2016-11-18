from flask import Flask
from flask import request
import os
from mongo import connect_mongo
from user import *
from errors import *
from jsonify import *
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
def list_users():
	users = get_users()
	clean_users = map(clean,users)
	print "woeifjowiejiwejfowiejfoij"
	print users
	print "woeifjowiejiwejfowiejfoij"
	return "True"



# SERVER START UP
if __name__ == "__main__":
	if "DEBUG" in os.environ:
		print "Entering Debug Mode..."
		debug = True
	else:
		debug = False

	app.run(debug=debug)