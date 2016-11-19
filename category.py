import mongo_burrito

def create_category(category_params):
	category = copy(category_params)
	ensure_create_category_fields(category)
	category.update({"_id":str(insert_category(category))}) # TODO add error handling
	clean(category)
	validate_all_required_fields(category)
	return category 

# def create_subcategory(subcategory_params):

def ensure_create_category_fields(category_params):
	for category_param in CREATE_CATEGORY_FIELDS:
		if category_param not in category_params:
			error_bad_request("Missing Field: " + category_param)	

def clean_category(category): 
	for field in SUPPORTED_USER_FIELDS:
		if field=="_id":
			if field in category:
				category[field] = str(category[field])
	return category
validate_all_required_fields

# Mongo Funcitons
def insert_user(user):
	return mongo_burrito.insert(user,"users")	

def get_users(query):
	return list(mongo_burrito.get(query,"users"))

def update_user(user_id,user_updates):
	return mongo_burrito.update({"_id":to_bson(user_id)},{"$set":user_updates},False,"users")

def delete_user(user_id):
	return mongo_burrito.delete({"_id":to_bson(user_id)},"users") 
