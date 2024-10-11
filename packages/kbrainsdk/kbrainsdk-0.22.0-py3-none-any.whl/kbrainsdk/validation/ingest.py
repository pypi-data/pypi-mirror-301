from kbrainsdk.validation.common import get_payload, validate_required_parameters

def validate_ingest_focused_chat(req):
    body = get_payload(req)
    focused_chat_id = body.get('focused_chat_id')
    assertion_token = body.get('assertion_token')
    client_secret = body.get('client_secret')
    client_id = body.get('client_id')
    tenant_id = body.get('tenant_id')

    required_arguments = ["focused_chat_id", "assertion_token", "client_secret", "client_id", "tenant_id"]
    validate_required_parameters(body, required_arguments)
    
    return focused_chat_id, assertion_token, client_secret, client_id, tenant_id

def validate_ingest_status(req):
    body = get_payload(req)
    focused_chat_id = body.get('focused_chat_id')

    required_arguments = ["focused_chat_id"]
    validate_required_parameters(body, required_arguments)
    
    return focused_chat_id