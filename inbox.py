from mongo import *
from constants import *

def setup_inbox(user):
	user["inbox_id"] = insert_inbox(new_inbox())

def new_inbox():
	return {
		"messages": []
	}

def insert_inbox(inbox):
	return insert(inbox,"inboxes")	
