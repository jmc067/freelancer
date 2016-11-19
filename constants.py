# Authentication Constants
AUTHENTICATION_FIELDS = ["email","password"]

# User Constants
SENSITIVE_USER_FIELDS = ["password"]
SUPPORTED_USER_ROLES = ["CLIENT","WORKER","ADMIN"]
SIGNUP_USER_FIELDS = ["email","first_name","last_name","role"]
AUTO_GENERATED_USER_FIELDS = ["_id","inbox_id","ledger_id","salted_password"]
SUPPORTED_USER_FIELDS = SIGNUP_USER_FIELDS + AUTO_GENERATED_USER_FIELDS 
EDITABLE_USER_FIELDS = ["first_name","last_name","email"]
REQUIRED_USER_FIELDS = [field for field in SUPPORTED_USER_FIELDS if field not in SENSITIVE_USER_FIELDS] 

# Category Constants
SENSITIVE_CATEGORY_FIELDS = []
CREATE_CATEGORY_FIELDS = ["name","description"]
AUTO_GENERATED_CATEGORY_FIELDS = ["_id"]
SUPPORTED_CATEGORY_FIELDS = CREATE_CATEGORY_FIELDS + AUTO_GENERATED_CATEGORY_FIELDS 
EDITABLE_CATEGORY_FIELDS = ["name","description"]
REQUIRED_CATEGORY_FIELDS = [field for field in SUPPORTED_CATEGORY_FIELDS if field not in SENSITIVE_CATEGORY_FIELDS] 


# Session Constants
SECS_IN_AN_HOUR = 3600
SESSION_LENGTH = SECS_IN_AN_HOUR * 2

# BSON Constants
BSON_FIELDS = ["_id","inbox_id","ledger_id"]

# Route Constants
PUBLIC_ROUTES = ["/","/user/signup","/user/login"]