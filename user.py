from mongo import *

def store_user(user):
	return insert({"last_name":"Colina"},"users")	
