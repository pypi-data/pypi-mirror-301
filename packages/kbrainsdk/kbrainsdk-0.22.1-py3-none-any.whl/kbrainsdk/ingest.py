import re
from uuid import uuid4 as uuid_generator
from kbrainsdk.validation.ingest import validate_ingest_status, validate_ingest_focused_chat
from kbrainsdk.apibase import APIBase

class Ingest(APIBase):

    def __init__(self, *args, **kwds):
        return super().__init__(*args, **kwds)


    def get_status(self, focused_chat_id):
        payload = {
            "focused_chat_id": focused_chat_id
        }

        validate_ingest_status(payload)

        path = f"/ingest/status/v2"
        response = self.apiobject.call_endpoint(path, payload, "post")
        return response
    
    def ingest_focused_chat(
            self, 
            focused_chat_id:str,
            assertion_token:str,         
            client_secret:str,         
            client_id:str, 
            tenant_id:str, 
        ) -> str:

        payload = {
            "focused_chat_id": focused_chat_id,
            "assertion_token": assertion_token,
            "client_secret": client_secret,
            "client_id": client_id,
            "tenant_id": tenant_id
        }

        validate_ingest_focused_chat(payload)

        path = "/ingest/focused-chat/v1"
        response = self.apiobject.call_endpoint(path=path, payload=payload, method="post")
        return response
    
    def convert_site_to_datasource(self, site):
        # Remove special characters and replace spaces with hyphens
        site_name = re.sub(r'[^a-zA-Z0-9\s]', '', site)
        site_name = site_name.replace(' ', '-')
        return f"sharepoint-{site_name.lower().replace('.', '-')}"

    def convert_email_to_datasource(self, email):
        return f"drive-{email.lower().replace('@', '-at-').replace('.', '-')}"
    
