
# Returns Error Bad Request (400)
def error_bad_request(message):
	abort(400,format_message(message))
