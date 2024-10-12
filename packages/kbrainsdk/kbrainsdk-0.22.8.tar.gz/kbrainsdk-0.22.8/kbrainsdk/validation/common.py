import re

class ResourceConflictException(Exception):
    pass
class APIKeyException(Exception):
    pass
class AccessDeniedException(APIKeyException):
    pass
class HTTP429Error(Exception):
    pass

def validate_email(email):
    # Define a regular expression for email validation
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    # Return True if the email matches the regex, False otherwise
    return re.match(email_regex, email) is not None


def validate_scopes(user_scopes, acceptable_scopes):
    has_scope = False
    for user_scope in user_scopes:
        if user_scope == "godmode":
            has_scope = True
            break 
        
        if user_scope in acceptable_scopes:
            has_scope = True
            break

    if not has_scope:
        raise APIKeyException("User does not have appropriate access scopes for this endpoint")

def validate_required_parameters(body, required_arguments):
    missing_values = [value for value in required_arguments if value not in body]
    if missing_values:
        raise ValueError("Missing or empty parameter in request body. Requires: {}".format(", ".join(missing_values)))

def get_payload(req):
    if type(req) == dict:
        return req
    
    return req.get_json()