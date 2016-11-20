# Authentication Constants
AUTHENTICATION_FIELDS = ["email","password"]

# User Constants
SENSITIVE_USER_FIELDS = ["password"]
SUPPORTED_USER_ROLES = ["CLIENT","WORKER","ADMIN"]
SIGNUP_USER_FIELDS = ["email","first_name","last_name","role"]
OPTIONAL_USER_FIELDS = ["photo","categories","subcategories"]  # TODO include this in user creation/edit.  Make sure its an image? or png? 
AUTO_GENERATED_USER_FIELDS = ["_id","inbox_id","ledger_id","salted_password"]
SUPPORTED_USER_FIELDS = SIGNUP_USER_FIELDS + AUTO_GENERATED_USER_FIELDS + OPTIONAL_USER_FIELDS
EDITABLE_USER_FIELDS = ["first_name","last_name","email","photo","categories","subcategories"]
REQUIRED_USER_FIELDS = [field for field in SUPPORTED_USER_FIELDS if field not in SENSITIVE_USER_FIELDS] 

# Category Constants
SENSITIVE_CATEGORY_FIELDS = []
CREATE_CATEGORY_FIELDS = ["name"]
OPTIONAL_CATEGORY_FIELDS = ["description"]
AUTO_GENERATED_CATEGORY_FIELDS = ["_id"]
SUPPORTED_CATEGORY_FIELDS = CREATE_CATEGORY_FIELDS + AUTO_GENERATED_CATEGORY_FIELDS + OPTIONAL_CATEGORY_FIELDS
EDITABLE_CATEGORY_FIELDS = ["name","description"]
REQUIRED_CATEGORY_FIELDS = [field for field in SUPPORTED_CATEGORY_FIELDS if field not in SENSITIVE_CATEGORY_FIELDS] 

# SubCategory Constants
SENSITIVE_SUBCATEGORY_FIELDS = []
CREATE_SUBCATEGORY_FIELDS = ["name","parent_category"]
OPTIONAL_SUBCATEGORY_FIELDS = ["description"]
AUTO_GENERATED_SUBCATEGORY_FIELDS = ["_id"]
SUPPORTED_SUBCATEGORY_FIELDS = CREATE_SUBCATEGORY_FIELDS + AUTO_GENERATED_SUBCATEGORY_FIELDS + OPTIONAL_SUBCATEGORY_FIELDS
EDITABLE_SUBCATEGORY_FIELDS = ["name","description","parent_category"]
REQUIRED_SUBCATEGORY_FIELDS = [field for field in SUPPORTED_SUBCATEGORY_FIELDS if field not in SENSITIVE_SUBCATEGORY_FIELDS] 

# Session Constants
SECS_IN_AN_HOUR = 3600
SESSION_LENGTH = SECS_IN_AN_HOUR * 2

# BSON Constants
BSON_FIELDS = ["_id","inbox_id","ledger_id"]

# Route Constants
PUBLIC_ROUTES = ["/","/user/signup","/user/login"]