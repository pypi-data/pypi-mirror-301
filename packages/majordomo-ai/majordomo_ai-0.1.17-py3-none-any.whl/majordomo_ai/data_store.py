import os
import requests
import json
from .auth import *
from .models import *

def CreateVectorDBDataStore(data_store_name, 
                            vectordb_profile,
                            embedding_model,
                            shared):

    """Create a Vector Database. Once it is created with an embedding model, it cannot be changed as
    all documents will need to use the same model to get consistent results

    Parameters
    ----------
    md_api_key : Majordomo API Key.
    data_store_name : Name of the data store (This is also the name of the index in the vector database)
    vectordb_profile : The name of the Vector DB profile that will be used to retrieve the 
        connection parameters for the vector database.
    embedding_model : The embedding model to use for creation of text or multi-modal embeddings.
    shared : Whether this data store can be used by other users for querying.

    Returns
    -------
    JSON response with the following information.
        status : 0 indicates success, any other number indicates failure.
        error : Indicates the error response.
    """

    director_url = os.environ['MAJORDOMO_AI_DIRECTOR']

    response = {}
    json_input = {}
    json_input['name'] = data_store_name
    try:
        json_input['credentials'] = CreateCredentials()
    except Exception as e: raise

    json_input['type'] = DataStoreTypeEnum.VectorDB
    json_input['embedding_model'] = embedding_model
    json_input['vectordb_profile'] = vectordb_profile
    json_input['shared'] = shared

    try:
        headers = {"Content-Type": "application/json"}
        result = requests.post(director_url + '/data_store', data=json.dumps(json_input), headers=headers)
        if result.status_code != 200:
            return MdErrorResponse(result.content.decode("utf-8"))
        else:
            return MdSuccessResponse("")

    except Exception as e:
        return MdErrorResponse(str(e))

def UpdateVectorDBDataStore(data_store_name, **kwargs):
    """Create a Vector Database. Once it is created with an embedding model, it cannot be changed as
    all documents will need to use the same model to get consistent results

    Mandatory Parameters
    --------------------
    data_store_name : Name of the data store (This is also the name of the index in the vector database)

    Optional Parameters
    --------------------
    shared : Whether this data store can be used by other users for querying.

    Returns
    -------
    JSON response with the following information.
        status : 0 indicates success, any other number indicates failure.
        error : Indicates the error response.
    """
    director_url = os.environ['MAJORDOMO_AI_DIRECTOR']

    response = {}

    json_input = {}
    json_input['name'] = data_store_name
    try:
        json_input['credentials'] = CreateCredentials()
    except Exception as e: 
        return MdErrorResponse(str(e))

    shared = kwargs.get('shared', None)

    if shared is None:
        return MdErrorResponse("No updatable options provided")

    json_input['shared'] = shared

    try:
        headers = {"Content-Type": "application/json"}
        result = requests.put(director_url + '/data_store', data=json.dumps(json_input), headers=headers)
        if result.status_code != 200:
            return MdErrorResponse(result.content.decode("utf-8"))
        else:
            return MdSuccessResponse("")
    except Exception as e: 
        return MdErrorResponse(str(e))

def CreateStructuredDBDataStore(data_store_name, 
                                data_store_type,
                                db_url, 
                                db_name, 
                                db_table):

    """Create or update an Structered Data Store. A structured store is a placeholder for connecting
    to any database like an SQL or MongoDB that will server as the data source for a natural language
    to database query.

    Parameters
    ----------
    data_store_name : Name of the data store (This is also the name of the index in the vector database)
    data_store_type : The database type. Valid values : 
        md.DataStoreTypeEnum.SQL 
        md.DataStoreTypeEnum.Mongo 
    db_url : The URL of the database. 
    db_name : The name of the database, either in SQL or Mongo.
    db_table : The name of the table (or a collection or any sub-category) of the database.

    Returns
    -------
    JSON response with the following information.
        status : 0 indicates success, any other number indicates failure.
        error : Indicates the error response.
    """

    director_url = os.environ['MAJORDOMO_AI_DIRECTOR']


    response = {}
    json_input = {}
    json_input['name'] = data_store_name
    try:
        json_input['credentials'] = CreateCredentials()
    except Exception as e: 
        return MdErrorResponse(str(e))

    json_input['type'] = data_store_type
    json_input['vectordb_profile'] = ''
    json_input['db_url'] = db_url
    json_input['db_name'] = db_name
    json_input['db_table'] = db_table
    json_input['shared'] = False

    try:
        headers = {"Content-Type": "application/json"}
        result = requests.post(director_url + '/data_store', data=json.dumps(json_input), headers=headers)
        if result.status_code != 200:
            return MdErrorResponse(result.content.decode("utf-8"))
        else:
            return MdSuccessResponse("")

    except Exception as e: 
        return MdErrorResponse(str(e))

def UpdateStructuredDBDataStore(data_store_name, **kwargs):
    """Create a Vector Database. Once it is created with an embedding model, it cannot be changed as
    all documents will need to use the same model to get consistent results

    Mandatory Parameters
    --------------------
    data_store_name : Name of the data store (This is also the name of the index in the vector database)

    Optional Parameters
    --------------------
    db_url : The URL of the database. 
    db_name : The name of the database, either in SQL or Mongo.
    db_table : The name of the table (or a collection or any sub-category) of the database.

    Returns
    -------
    JSON response with the following information.
        status : 0 indicates success, any other number indicates failure.
        error : Indicates the error response.
    """
    director_url = os.environ['MAJORDOMO_AI_DIRECTOR']

    response = {}

    json_input = {}
    json_input['name'] = data_store_name
    try:
        json_input['credentials'] = CreateCredentials()
    except Exception as e: 
        return MdErrorResponse(str(e))

    for key, value in kwargs.items():
        match key:
            case 'db_url':
                json_input['db_url'] = value
            case 'db_name':
                json_input['db_name'] = value
            case 'db_table':
                json_input['db_table'] = value

    try:
        headers = {"Content-Type": "application/json"}
        result = requests.put(director_url + '/data_store', data=json.dumps(json_input), headers=headers)
        if result.status_code != 200:
            return MdErrorResponse(result.content.decode("utf-8"))
        else:
            return MdSuccessResponse("")

    except Exception as e: 
        return MdErrorResponse(str(e))

def DeleteDataStore(name):
       
    """Delete a Data Store. Incase of a vector database, this deletes the embedding vector database. Incase of 
    structured database type, this does not delete any customer owned database that was used for querying. In case
    of unified database also, this will only delete the vector database.

    Parameters
    ----------
    name : Name of the data store (This is also the name of the index in the vector database)

    Returns
    -------
    JSON response with the following information.
        status : 0 indicates success, any other number indicates failure.
        error : Indicates the error response.
    """

    director_url = os.environ['MAJORDOMO_AI_DIRECTOR']

    response = {}
    json_input = {}
    try:
        json_input['credentials'] = CreateCredentials()
    except Exception as e: 
         return MdErrorResponse(str(e))

    json_input['name'] = name

    try:
        headers = {"Content-Type": "application/json"}
        result = requests.delete(director_url + '/data_store', data=json.dumps(json_input), headers=headers)

        if result.status_code != 200:
            return MdErrorResponse(result.content.decode("utf-8"))
        else:
            return MdSuccessResponse("")

    except Exception as e:
         return MdErrorResponse(str(e))

def GetDataStores(data_store_type, name):

    """Get list of Data Stores. 

    Parameters
    ----------
    None

    Returns
    -------
    JSON response with the following information.
        status : 0 indicates success, any other number indicates failure.
        error : Indicates the error response.
    """

    director_url = os.environ['MAJORDOMO_AI_DIRECTOR']

    response = {}
    json_input = {}
    try:
        json_input['credentials'] = CreateCredentials()
    except Exception as e: 
         return MdErrorResponse(str(e))

    try:
        headers = {"Content-Type": "application/json"}

        query_string = ""
        if data_store_type != 0:
            query_string = f"type={data_store_type}"

        if name != "":
            if query_string != "":
                query_string = query_string + "&&"
            query_string = query_string + f"name={name}"

        if query_string != "":
            result = requests.get(director_url + f'/data_store?{query_string}', data=json.dumps(json_input), headers=headers)
        else:
            result = requests.get(director_url + '/data_store', data=json.dumps(json_input), headers=headers)

        if result.status_code != 200:
            return MdErrorResponse(result.content.decode("utf-8"))
        else:
            return MdSuccessResponse(result.content.decode("utf-8"))

    except Exception as e: 
         return MdErrorResponse(str(e))

def DataStoreIngest(data_store_name, 
                    input_type, 
                    input_filter, 
                    ingest_type, 
                    ingest_params, 
                    **kwargs):

    """Add a document to the Data Store as a one time activity.

    Parameters
    ----------
    data_store : Name of the data store.
    input_type : This is the source of the document. Valid values are,
        md.InputTypeEnum.AWSS3
        md.InputTypeEnum.AzureBlob
        md.InputTypeEnum.Webpage
        md.InputTypeEnum.Local
    input_filter : A JSON describing the location of the file. Examples for 
         different types are below.
         {"files" : "abcd.pdf", "region": "us-east-1", "bucket": "demo"}
         {"url" : "http://abcd.pdf"}
    ingest_type : The type of ingestion to be performed. Valid values are,
        md.IngestTypeEnum.Text
        md.IngestTypeEnum.Image
    ingest_params : A JSON describing any special ingestion parameters.

    Returns
    -------
    JSON response with the following information.
        status : 0 indicates success, any other number indicates failure.
        error : Indicates the error response.
    """

    director_url = os.environ['MAJORDOMO_AI_DIRECTOR']

    json_input = {}

    json_input['name'] = ''
    try:
        json_input['credentials'] = CreateCredentials()
    except Exception as e: 
         return MdErrorResponse(str(e))

    json_input['input_type'] = input_type
    json_input['input_filter'] = input_filter
    json_input['data_store'] = data_store_name
    json_input['ingest_params'] = ingest_params
    json_input['ingest_type'] = ingest_type

    if ingest_params != "":
        try:
            json.loads(json_input['ingest_params']) 
        except Exception as e:
            return MdErrorResponse(str(e))

    if input_filter != "":
        try:
            infoMap = json.loads(input_filter)
        except Exception as e:
             return MdErrorResponse(str(e))

        try:
            "files" in infoMap
        except Exception as e: 
             return MdErrorResponse(str(e))

    if input_type == InputTypeEnum.Local:
        try:
            files = {
                 'json': ("", json.dumps(json_input), 'application/json'),
                 'file': (infoMap["files"], open(infoMap["files"],'rb'), 'application/octet-stream')
            }

            result = requests.post(director_url + '/file_upload', files=files)
            if result.status_code != 200:
                return MdErrorResponse(result.content.decode("utf-8"))
            else:
                return MdSuccessResponse("")

        except Exception as e:
         return MdErrorResponse(str(e))

    for key, value in kwargs.items():
        match key:
            case 'input_keys':
                json_input['input_keys'] = value

    try:
        headers = {"Content-Type": "application/json"}
        result = requests.post(director_url + '/data_store_ingest', data=json.dumps(json_input), headers=headers)
        if result.status_code != 200:
            return MdErrorResponse(result.content.decode("utf-8"))
        else:
            return MdSuccessResponse("")

    except Exception as e: 
         return MdErrorResponse(str(e))

def DataStoreQuery(query_type,
                   data_store,
                   embedding_model,
                   llm_model,
                   query_params,
                   query_str):

    """Query a document using the Data Store as a one time activity.

    Parameters
    ----------
    query_type : This is the type of query to be executed. Valid values are:
        md.QueryTypeEnum.Text
        md.QueryTypeEnum.Image
        md.QueryTypeEnum.SQL
    data_stores : List of data stores.
    llm_model : Specify the LLM model to be used for the query. This should be
        permitted for this user in model profile.
    query_params : A JSON describing any special ingestion parameters.
    query_str : The actual query string. As of now, variable expansion within the string
        is not supported. Please do that operation outside this call and supply the final
        query string. Query string may contain indications to the model about the format of
        the output. But honoring that accurately will be the purview of the LLM model.

    Returns
    -------
    JSON response with the following information.
        status : 0 indicates success, any other number indicates failure.
        error : Indicates the error response.
        response : Indicates the query response.
    """

    director_url = os.environ['MAJORDOMO_AI_DIRECTOR']

    json_input = {}
    try:
        json_input['credentials'] = CreateCredentials()
    except Exception as e: 
         return MdErrorResponse(str(e))

    json_input['data_store'] = data_store
    json_input['query_type'] = query_type
    json_input['llm_model'] = llm_model
    json_input['embedding_model'] = embedding_model
    json_input['query_params'] = query_params
    json_input['query_str'] = query_str

    try:
        headers = {"Content-Type": "application/json"}
        result = requests.post(director_url + '/data_store_query', data=json.dumps(json_input), headers=headers)
        if result.status_code != 200:
            return MdErrorResponse(result.content.decode("utf-8"))
        else:
            return MdSuccessResponse(result.content.decode("utf-8"))

    except Exception as e:
         return MdErrorResponse(str(e))
