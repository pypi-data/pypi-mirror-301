import os
import json
import requests
from .auth import *
from .models import *

from pathlib import Path

def CreateIngestPipeline(ingestion_pipeline_name,
                       data_store_name,
                       input_type,
                       input_filter,
                       ingest_type,
                       ingest_params,
                       timer_interval,
                       timer_on):
       

    director_url = os.environ['MAJORDOMO_AI_DIRECTOR']

    json_input = {}

    try:
        json_input['credentials'] = CreateCredentials()
    except Exception as e: 
         return MdErrorResponse(str(e))

    json_input['data_store'] = data_store_name
    json_input['name'] = ingestion_pipeline_name
    json_input['input_type'] = input_type
    json_input['input_filter'] = input_filter
    json_input['ingest_type'] = ingest_type
    json_input['ingest_params'] = ingest_params
    json_input['timer_interval'] = timer_interval
    json_input['timer_on'] = timer_on

    try:
        ingest_params = json.loads(json_input['ingest_params']) 
    except Exception as e:
         return MdErrorResponse(str(e))

    for key, value in kwargs.items():
        match key:
            case 'input_keys':
                json_input['input_keys'] = value

    try:
        headers = {"Content-Type": "application/json"}
        result = requests.post(director_url + '/ingest_pipeline', data=json.dumps(json_input), headers=headers)
        if result.status_code != 200:
            return MdErrorResponse(result.content.decode("utf-8"))
        else:
            return MdSuccessResponse("")

    except Exception as e: 
         return MdErrorResponse(str(e))

def UpdateIngestPipeline(ingestion_pipeline_name,
                         data_store_name,
                         **kwargs):

    director_url = os.environ['MAJORDOMO_AI_DIRECTOR']

    json_input = {}

    try:
        json_input['credentials'] = CreateCredentials()
    except Exception as e: 
         return MdErrorResponse(str(e))

    json_input['data_store'] = data_store_name
    json_input['name'] = ingestion_pipeline_name
    for key, value in kwargs.items():
        match key:
            case 'input_filter':
                json_input['input_filter'] = value
            case 'input_keys':
                json_input['input_keys'] = value
            case 'ingest_params':
                json_input['ingest_params'] = ingest_params
                try:
                    ingest_params = json.loads(json_input['ingest_params']) 
                except Exception as e:
                     return MdErrorResponse(str(e))
            case 'timer_interval':
                json_input['timer_interval'] = value
            case 'timer_on':
                json_input['timer_on'] = value

    try:
        headers = {"Content-Type": "application/json"}
        result = requests.put(director_url + '/ingest_pipeline', data=json.dumps(json_input), headers=headers)
        if result.status_code != 200:
            return MdErrorResponse(result.content.decode("utf-8"))
        else:
            return MdSuccessResponse("")

    except Exception as e:
         return MdErrorResponse(str(e))

def DeleteIngestPipeline(name, data_store):
       
    director_url = os.environ['MAJORDOMO_AI_DIRECTOR']

    json_input = {}

    try:
        json_input['credentials'] = CreateCredentials()
    except Exception as e: 
         return MdErrorResponse(str(e))

    json_input['name'] = name
    json_input['data_store'] = data_store

    try:
        headers = {"Content-Type": "application/json"}
        result = requests.delete(director_url + '/ingest_pipeline', data=json.dumps(json_input), headers=headers)
        if result.status_code != 200:
            return MdErrorResponse(result.content.decode("utf-8"))
        else:
            return MdSuccessResponse("")

    except Exception as e:
         return MdErrorResponse(str(e))

def IngestPipelineRun(data_store, ingest_pipeline):

    director_url = os.environ['MAJORDOMO_AI_DIRECTOR']

    json_input = {}

    try:
        json_input['credentials'] = CreateCredentials()
    except Exception as e:
         return MdErrorResponse(str(e))

    json_input['data_store'] = data_store
    json_input['name'] = ingest_pipeline

    try:
        headers = {"Content-Type": "application/json"}
        result = requests.post(director_url + '/ingest_pipeline_run', data=json.dumps(json_input), headers=headers)
        if result.status_code != 200:
            return MdErrorResponse(result.content.decode("utf-8"))
        else:
            return MdSuccessResponse("")
        return result

    except Exception as e:
         return MdErrorResponse(str(e))

