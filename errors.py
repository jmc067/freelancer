from flask import abort

def error_bad_request(message):
	abort(400,{ "message": message })
