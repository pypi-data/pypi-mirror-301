from kbrainsdk.validation.common import get_payload, validate_email, validate_required_parameters
from typing import List 

def validate_list_datasets(req):
    body = get_payload(req)
    email = body.get('email')
    token = body.get('token')
    client_id = body.get('client_id')
    oauth_secret = body.get('oauth_secret')
    tenant_id = body.get('tenant_id')
    search_term = body.get('search_term')

    focus_chat_id = None
    if "focus_chat_id" in body:
        focus_chat_id = body.get('focus_chat_id')

    selected_datasets = None
    if body.get('selected_datasets'):
        selected_datasets = body.get('selected_datasets')
        if selected_datasets == []:
            selected_datasets = None


    # Validate parameters
    if not all([email, token, client_id, oauth_secret, tenant_id]):
        raise ValueError("Missing or empty parameter in request body. Expecting email, token, client_id, oauth_secret, tenant_id")

    if not validate_email(email):
        raise ValueError("Invalid email address")
    
    return email, token, client_id, oauth_secret, tenant_id, selected_datasets, search_term, focus_chat_id

def validate_search_datasets(req):
    body = get_payload(req)
    query = body.get('query')
    topic = body.get('topic')
    citations = body.get('citations')

    # Validate parameters
    if not all([query, topic, citations]):
        raise ValueError("Missing or empty parameter in request body. Expecting query, topic, citations")

    if not isinstance(citations, int):
        raise ValueError("Citations must be an integer")

    return query, topic, citations

def validate_list_dataset_files(req):
    body = get_payload(req)
    email = body.get('email')
    token = body.get('token')
    client_id = body.get('client_id')
    oauth_secret = body.get('oauth_secret')
    tenant_id = body.get('tenant_id')
    dataset_id = body.get('dataset_id')
    pagination = None
    search_term = None
    if "search_term" in body:
        search_term = body.get('search_term')

    if "pagination" in body:
        pagination = body.get('pagination')
    
    max_item_count = 10
    if "max_item_count" in body:
        max_item_count = body.get('max_item_count')

    # Validate parameters
    if not all([email, token, client_id, oauth_secret, tenant_id, dataset_id]):
        raise ValueError("Missing or empty parameter in request body. Expecting email, token, client_id, oauth_secret, tenant_id, dataset_id")

    if not validate_email(email):
        raise ValueError("Invalid email address")
    
    return email, token, client_id, oauth_secret, tenant_id, dataset_id, pagination, max_item_count, search_term

def validate_list_focus_configurations(req):
    body = get_payload(req)
    token = body.get('token')
    client_id = body.get('client_id')
    oauth_secret = body.get('oauth_secret')
    tenant_id = body.get('tenant_id')

    search_term = None
    if "search_term" in body:
        search_term = body.get('search_term')

    # Validate parameters
    if not all([token, client_id, oauth_secret, tenant_id]):
        raise ValueError("Missing or empty parameter in request body. Expecting token, client_id, oauth_secret, tenant_id")
    
    return token, client_id, oauth_secret, tenant_id, search_term    

def validate_get_focus_configuration(req):
    body = get_payload(req)
    token = body.get('token')
    client_id = body.get('client_id')
    oauth_secret = body.get('oauth_secret')
    tenant_id = body.get('tenant_id')
    focus_chat_id = body.get('focus_chat_id')

    # Validate parameters
    if not all([token, client_id, oauth_secret, tenant_id, focus_chat_id]):
        raise ValueError("Missing or empty parameter in request body. Expecting token, client_id, oauth_secret, tenant_id, focus_chat_id")
    
    return token, client_id, oauth_secret, tenant_id, focus_chat_id

def validate_update_focus_configuration(req):
    body = get_payload(req)
    token = body.get('token')
    client_id = body.get('client_id')
    oauth_secret = body.get('oauth_secret')
    tenant_id = body.get('tenant_id')
    focus_chat_id = body.get('focus_chat_id')
    configuration = body.get('configuration')

    # Validate parameters
    if not all([token, client_id, oauth_secret, tenant_id, focus_chat_id]):
        raise ValueError("Missing or empty parameter in request body. Expecting token, client_id, oauth_secret, tenant_id, focus_chat_id")
    
    if "groups" in configuration:
        if not isinstance(configuration["groups"], list):
            raise ValueError("'groups' property must be a list")
    
    if "admin_group" in configuration:
        raise ValueError("'admin_group' property cannot be modified")

    if "prompt" in configuration:
        if not isinstance(configuration["prompt"], str):
            raise ValueError("'prompt' property must be a string")
    
    if "datasets" in configuration:
        if not isinstance(configuration["datasets"], list):
            raise ValueError("'datasets' property must be a list")
        
    #Raise a ValueError if any other property is in the payload
    for key in configuration:
        if key not in ["groups", "admin_group", "prompt", "datasets"]:
            raise ValueError(f"Invalid property '{key}' in payload")

    return token, client_id, oauth_secret, tenant_id, focus_chat_id, configuration


def validate_upsert_focus_configuration_v2(req):
    
    body = get_payload(req)
    required_arguments = ["token", "client_id", "oauth_secret", "tenant_id", "focus_chat_id", "configuration"]
    validate_required_parameters(body, required_arguments)

    token = body.get('token')
    client_id = body.get('client_id')
    oauth_secret = body.get('oauth_secret')
    tenant_id = body.get('tenant_id')
    focus_chat_id = body.get('focus_chat_id')
    configuration = body.get('configuration')

    if not "display_name" in configuration:
        raise ValueError("'display_name' property in configuration object is required and must be a string.")
    
    if not isinstance(configuration["display_name"], str):
        raise ValueError("'display_name' property in configuration object must be a string.")
    
    if not "index" in configuration:
        raise ValueError("'index' property in configuration object is required and must be a string.")

    if not isinstance(configuration["index"], str):
        raise ValueError("'index' property in configuration object must be a string.")
    
    if not "groups" in configuration:
        raise ValueError("'groups' property is required")
    
    if not isinstance(configuration["groups"], list):
       raise ValueError("'groups' property must be included in the configuration object and must be a list")
    
    if not "admin_group" in configuration:
        raise ValueError("'admin_group' property must be included in the configuration object and must be a string representation of the entra group object id.")
    
    if not isinstance(configuration["admin_group"], str):
        raise ValueError("'admin_group' property must be a string representation of the entra group object id.")

    if not "prompt" in configuration:
        raise ValueError("'prompt' property must be included in the configuration object and must be a string")

    if not isinstance(configuration["prompt"], str):
        raise ValueError("'prompt' property must be a string")

    if not "sites" in configuration:
        raise ValueError("'sites' property must be included in the configuration object and must be a list of site objects containing the host and site properties") 
       
    if not isinstance(configuration["sites"], list):
            raise ValueError("'sites' property must be a list of site objects containing the host and site properties")
    
    for site in configuration["sites"]:
        if not "host" in site:
            raise ValueError(f"Invalid object in sites list. 'host' property must be included in the site object and must be a string. Invalid object: {site}")
        if not "site" in site:
            raise ValueError(f"Invalid object in sites list. 'site' property must be included in the site object and must be a string. Invalid object: {site}")

    #Raise a ValueError if any other property is in the payload
    for key in configuration:
        if key not in ["groups", "admin_group", "prompt", "sites", "index", "description", "status", "operation_id", "substatus", "display_name"]:
            raise ValueError(f"Invalid property '{key}' in configuration payload")

    return token, client_id, oauth_secret, tenant_id, focus_chat_id, configuration

def validate_list_dataset_files_v2(req: dict) -> List[str]:
    body = get_payload(req)
    validate_required_parameters(body, ["token", "client_id", "client_secret", "tenant_id", "focused_chat_id", "site", "host"])
    pagination = body.get('pagination', None)
    max_item_count = body.get('max_item_count', None)
    search_term = body.get('search_term', None)
    return [*body.values(), pagination, max_item_count, search_term]

def validate_search_datasets_v2(req: dict) -> List[str]:
    body = get_payload(req)
    validate_required_parameters(body, ["query", "focused_chat_id", "token", "client_id", "client_secret", "tenant_id"])
    query = body.get('query')
    focused_chat_id = body.get('focused_chat_id')
    token = body.get('token')
    client_id = body.get('client_id')
    client_secret = body.get('client_secret')
    tenant_id = body.get('tenant_id')
    citations = body.get('citations', None)
    filenames = body.get('filenames', None)

    return query, focused_chat_id, token, client_id, client_secret, tenant_id, citations, filenames