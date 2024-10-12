from typing import List
from kbrainsdk.validation.datasets import validate_list_datasets, validate_search_datasets, validate_list_dataset_files, validate_get_focus_configuration, validate_update_focus_configuration, validate_list_focus_configurations, validate_upsert_focus_configuration_v2, validate_list_dataset_files_v2, validate_search_datasets_v2
from kbrainsdk.apibase import APIBase

class Datasets(APIBase):

    def list_datasets(self, email, token, client_id, oauth_secret, tenant_id, selected_datasets = None, search_term = None, focus_chat_id = None):
        
        payload = {
            "email": email,
            "token": token,
            "client_id": client_id,
            "oauth_secret": oauth_secret,
            "tenant_id": tenant_id,
            "search_term": search_term,
            "selected_datasets": selected_datasets,
            "focus_chat_id": focus_chat_id
        }

        validate_list_datasets(payload)

        path = f"/datasets/list/v1"
        response = self.apiobject.call_endpoint(path, payload, "post")
        return response

    
    def list_files_in_datasets(self, email, token, client_id, oauth_secret, tenant_id, dataset_id, pagination = None, max_item_count=10, search_term = None):
        
        payload = {
            "email": email,
            "token": token,
            "client_id": client_id,
            "oauth_secret": oauth_secret,
            "tenant_id": tenant_id,
            "dataset_id": dataset_id,
            "pagination": pagination,
            "max_item_count": max_item_count,
            "search_term": search_term
        }

        validate_list_dataset_files(payload)

        path = f"/datasets/files/v1"
        response = self.apiobject.call_endpoint(path, payload, "post")
        return response

    def search_datasets(self, query, topic, citations, email, token, client_id, oauth_secret, tenant_id, selected_datasets = None, focus_chat_id = None):
        
        payload = {
            "email": email,
            "token": token,
            "client_id": client_id,
            "oauth_secret": oauth_secret,
            "tenant_id": tenant_id,
            "query": query,
            "topic": topic,
            "citations": citations,
            "focus_chat_id": focus_chat_id
        }

        if selected_datasets:
            payload["selected_datasets"] = selected_datasets

        validate_list_datasets(payload)
        validate_search_datasets(payload)

        path = f"/datasets/search/v1"
        response = self.apiobject.call_endpoint(path, payload, "post")
        return response
    
    def list_focus_configurations(self, token, client_id, oauth_secret, tenant_id, search_term = None):

        payload = {
            "token": token,
            "client_id": client_id,
            "oauth_secret": oauth_secret,
            "tenant_id": tenant_id,
            "search_term": search_term
        }

        validate_list_focus_configurations(payload)


        path = f"/datasets/focus-configurations/v1"
        response = self.apiobject.call_endpoint(path, payload, method="post")
        return response
    
    def get_focus_configuration(self, token, client_id, oauth_secret, tenant_id, focus_chat_id):

        payload = {
            "token": token,
            "client_id": client_id,
            "oauth_secret": oauth_secret,
            "tenant_id": tenant_id,
            "focus_chat_id": focus_chat_id
        }

        validate_get_focus_configuration(payload)

        path = f"/datasets/get-focus-configuration/v1"
        response = self.apiobject.call_endpoint(path, payload, method="post")
        return response
    
    def update_focus_configuration(self, token, client_id, oauth_secret, tenant_id, focus_chat_id, configuration):

        payload = {
            "token": token,
            "client_id": client_id,
            "oauth_secret": oauth_secret,
            "tenant_id": tenant_id,
            "focus_chat_id": focus_chat_id,
            "configuration": configuration
        }

        validate_update_focus_configuration(payload)

        path = f"/datasets/update-focus-configuration/v1"
        response = self.apiobject.call_endpoint(path, payload, method="post")
        return response
    
    def list_focus_configurations_v2(self, token, client_id, oauth_secret, tenant_id, search_term = None):

        payload = {
            "token": token,
            "client_id": client_id,
            "oauth_secret": oauth_secret,
            "tenant_id": tenant_id,
            "search_term": search_term
        }

        validate_list_focus_configurations(payload)


        path = f"/datasets/focus-configurations/v2"
        response = self.apiobject.call_endpoint(path, payload, method="post")
        return response
    
    def get_focus_configuration_v2(self, token, client_id, oauth_secret, tenant_id, focus_chat_id):

        payload = {
            "token": token,
            "client_id": client_id,
            "oauth_secret": oauth_secret,
            "tenant_id": tenant_id,
            "focus_chat_id": focus_chat_id
        }

        validate_get_focus_configuration(payload)

        path = f"/datasets/get-focus-configuration/v2"
        response = self.apiobject.call_endpoint(path, payload, method="post")
        return response

    def update_focus_configuration_v2(self, token, client_id, oauth_secret, tenant_id, focus_chat_id, configuration):

        payload = {
            "token": token,
            "client_id": client_id,
            "oauth_secret": oauth_secret,
            "tenant_id": tenant_id,
            "focus_chat_id": focus_chat_id,
            "configuration": configuration
        }

        validate_upsert_focus_configuration_v2(payload)

        path = f"/datasets/update-focus-configuration/v2"
        response = self.apiobject.call_endpoint(path, payload, method="post")
        return response
    
    def list_files_in_datasets_v2(
            self,  
            token:str, 
            client_id:str, 
            client_secret:str, 
            tenant_id:str, 
            focused_chat_id:str, 
            site:str, 
            host:str, 
            pagination:str|None = None,
            max_item_count:int=10,
            search_term:str|None = None
        ) -> dict:
        



        payload = {
            "token": token,
            "client_id": client_id,
            "client_secret": client_secret,
            "tenant_id": tenant_id,
            "focused_chat_id": focused_chat_id,
            "site": site,
            "host": host,
        }

        validate_list_dataset_files_v2(payload)

        if pagination:
            payload["pagination"] = pagination
        
        if search_term:
            payload["search_term"] = search_term

        if max_item_count:
            payload["max_item_count"] = max_item_count

        path = f"/datasets/files/v2"
        response = self.apiobject.call_endpoint(path=path, payload=payload, method="post")
        return response

    def search_datasets_v2(
            self, 
            query:str, 
            focused_chat_id:str,            
            token:str,
            client_id:str,
            client_secret:str,
            tenant_id:str,
            citations:int=1,
            filenames:List[str]|None=None    
):
        
        payload = {
            "query": query,
            "focused_chat_id": focused_chat_id,            
            "token": token,
            "client_id": client_id,
            "client_secret": client_secret,
            "tenant_id": tenant_id,
            "citations": citations,            
        }

        if filenames:
            payload["filenames"] = filenames

        validate_search_datasets_v2(payload)

        path = f"/datasets/search/v2"
        response = self.apiobject.call_endpoint(path, payload, "post")
        return response