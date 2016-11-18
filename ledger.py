from mongo import *
from constants import *

def setup_ledger(user):
	user["ledger_id"] = insert_ledger(new_ledger())

def new_ledger():
	return {
		"logs": []
	}

def insert_ledger(ledger):
	return insert(ledger,"ledgers")	
