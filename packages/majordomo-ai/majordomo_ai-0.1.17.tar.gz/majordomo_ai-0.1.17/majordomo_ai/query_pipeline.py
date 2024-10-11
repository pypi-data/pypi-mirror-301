import os
import json
import requests
from .auth import *
from .models import *

from pathlib import Path

def CreateQueryPipeline(query_pipeline_name,
                        query_type,
                        data_stores,
                        embedding_model,
                        llm_model,
                        query_params):
       

    director_url = os.environ['MAJORDOMO_AI_DIRECTOR']

    json_input = {}

    json_input['name'] = query_pipeline_name
    try:
        json_input['credentials'] = CreateCredentials()
    except Exception as e:
         return MdErrorResponse(str(e))

    json_input['query_type'] = query_type
    json_input['data_stores'] = data_stores
    json_input['embedding_model'] = embedding_model
    json_input['llm_model'] = llm_model
    json_input['query_params'] = query_params

    try:
        headers = {"Content-Type": "application/json"}
        result = requests.post(director_url + '/query_pipeline', data=json.dumps(json_input), headers=headers)
        if result.status_code != 200:
            return MdErrorResponse(result.content.decode("utf-8"))
        else:
            return MdSuccessResponse("")

        return result

    except Exception as e:
         return MdErrorResponse(str(e))

def UpdateQueryPipeline(query_pipeline_name,
                        **kwargs):

    director_url = os.environ['MAJORDOMO_AI_DIRECTOR']

    json_input = {}

    try:
        json_input['credentials'] = CreateCredentials()
    except Exception as e: 
         return MdErrorResponse(str(e))

    json_input['name'] = query_pipeline_name
    for key, value in kwargs.items():
        match key:
            case 'data_stores':
                json_input['data_stores'] = value
            case 'query_params':
                json_input['query_params'] = value
            case 'embedding_model':
                json_input['embedding_model'] = value
            case 'llm_model':
                json_input['llm_model'] = value

    try:
        headers = {"Content-Type": "application/json"}
        result = requests.put(director_url + '/ingest_pipeline', data=json.dumps(json_input), headers=headers)
        if result.status_code != 200:
            return MdErrorResponse(result.content.decode("utf-8"))
        else:
            return MdSuccessResponse("")

    except Exception as e:
         return MdErrorResponse(str(e))

def DeleteQueryPipeline(query_pipeline_name):
       
    director_url = os.environ['MAJORDOMO_AI_DIRECTOR']

    json_input = {}
    try:
        json_input['credentials'] = CreateCredentials()
    except Exception as e:
         return MdErrorResponse(str(e))

    json_input['name'] = query_pipeline_name

    try:
        headers = {"Content-Type": "application/json"}
        result = requests.delete(director_url + '/query_pipeline', data=json.dumps(json_input), headers=headers)
        if result.status_code != 200:
            return MdErrorResponse(result.content.decode("utf-8"))
        else:
            return MdSuccessResponse("")

    except Exception as e:
         return MdErrorResponse(str(e))

def RunQueryPipeline(query_pipeline_name, query_str):

    director_url = os.environ['MAJORDOMO_AI_DIRECTOR']

    json_input = {}
    json_input['name'] = query_pipeline_name
    try:
        json_input['credentials'] = CreateCredentials()
    except Exception as e:
         return MdErrorResponse(str(e))

    json_input['query_str'] = query_str

    try:
        headers = {"Content-Type": "application/json"}
        result = requests.post(director_url + '/query_pipeline_run', data=json.dumps(json_input), headers=headers)
        if result.status_code != 200:
            return MdErrorResponse(result.content.decode("utf-8"))
        else:
            return MdSuccessResponse("")

    except Exception as e:
         return MdErrorResponse(str(e))

