import json

def to_json(whatever):
	return json.dumps(whatever)

def from_json(string):
	return json.loads(string)