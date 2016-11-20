import mongo_burrito
from constants import *

def setup_inbox(user):
	user["inbox_id"] = insert_inbox(new_inbox())

def new_inbox():
	return {
		"messages": []
	}

def insert_inbox(inbox):
	return mongo_burrito.insert(inbox,"inboxes")	

def get_inbox(query):
	return mongo_burrito.get(query,"inboxes")	
