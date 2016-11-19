SENSITIVE_USER_FIELDS = ["password"]
USER_SIGNUP_FIELDS = ["email","first_name","last_name","role"]
AUTO_GENERATED_USER_FIELDS = ["_id","inbox_id","ledger_id","salted_password"]
SUPPORTED_USER_FIELDS = USER_SIGNUP_FIELDS + AUTO_GENERATED_USER_FIELDS 

EDITABLE_USER_FIELDS = ["first_name","last_name","email"]

# Supported user fields minus the sensitive ones
REQUIRED_USER_FIELDS = [field for field in SUPPORTED_USER_FIELDS if field not in SENSITIVE_USER_FIELDS] 

SUPPORTED_ROLES = ["CLIENT","WORKER","ADMIN"]

AUTHENTICATION_FIELDS = ["email","password"]

HOUR = 3600
SESSION_LENGTH = HOUR * 2
