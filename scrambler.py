import bcrypt

def hash(string):
	return bcrypt.hashpw(str(string), bcrypt.gensalt())

def isMatch(string,hash):
	if bcrypt.hashpw(string, hash) == hash:
		return True
	else:
		return False