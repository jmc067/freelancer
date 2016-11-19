import bcrypt
import string
import random

def hash(string):
	return bcrypt.hashpw(str(string).encode('utf-8'), bcrypt.gensalt())

def is_match(string,hash):
	#  Needs to be utf8 encoded after being stored as text in mongo
	string = str(string).encode('utf-8')
	hash = hash.encode('utf-8')

	if bcrypt.hashpw(string, hash) == hash:
		return True
	else:
		return False

def scramble():
	return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))	

def utf8_encode(string):
	return string.encode('utf-8')