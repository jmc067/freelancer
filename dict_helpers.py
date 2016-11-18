import json

def copy(dictionary):
	new_dict = {}
	for key in dictionary:
		new_dict[key] = dictionary[key]
	return new_dict

def pretty_print(dictionary):
	print "{"
	for key in dictionary:
		print key + ": " + str(dictionary[key])
	print "}"


