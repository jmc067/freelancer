from flask import Flask
from flask import request
import os
from mongo import connect_mongo
from user import *
from errors import *
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
@app.route('/user', methods = ['POST'])
def new_user():
	return str(create_user(request.values))

# READ, UPDATE, DELETE user
@app.route('/user/<user_id>', methods = ['GET', 'POST', 'DELETE'])
def xxx(user_id):

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



# SERVER START UP
if __name__ == "__main__":
	if "DEBUG" in os.environ:
		print "Entering Debug Mode..."
		debug = True
	else:
		debug = False

	app.run(debug=debug)