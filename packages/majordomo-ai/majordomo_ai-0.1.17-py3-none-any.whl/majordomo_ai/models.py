from enum import Enum, IntEnum
from pydantic import BaseModel, ValidationError

###############################################################################
# Document Store                                                              #
###############################################################################

class InputTypeEnum(IntEnum):
    AWSS3 = 1
    AzureBlob = 2
    Webpage = 3
    Local = 4
    SQL = 5

###############################################################################
# Data Store                                                                  #
###############################################################################

class DataStoreTypeEnum(IntEnum):
    VectorDB = 1
    SQL = 2 
    MongoDB = 3

class DataStore(BaseModel): 
    id : str
    group : str
    workspace : str
    user_name :  str
    type : DataStoreTypeEnum
    name : str

    vectordb_profile : str
    embedding_model : str
    shared :   bool

    db_url :  str
    db_name : str
    db_table : str

class DataStoreList(BaseModel):
    data_stores : list[DataStore]

class DataStoreMessage(BaseModel):
    md_api_key : str
    name : str
    type : DataStoreTypeEnum

    vectordb_profile : str
    embedding_model :  str

    db_url : str
    db_name : str
    db_table : str

    shared : bool

###############################################################################
# Ingestion Pipeline                                                          #
###############################################################################

class TextIngestType(IntEnum):
    Base = 1 
    Summary = 2

class PDFExtractorTypeEnum(IntEnum):
    LlamaParse = 1
    PyMuPDF = 2
    PDF2Image = 3

class IngestTypeEnum(IntEnum):
    Text = 1
    Image = 2
    Custom = 3

class IngestPipeline(BaseModel):
    id : str
    group : str
    workspace : str
    user_name :  str
    name : str
    data_store : str
    input_type : InputTypeEnum
    input_filter : str
    input_keys : str
    ingest_type : IngestTypeEnum
    ingest_params : str
    timer_interval : int
    timer_on : int

class IngestPipelineMessage(BaseModel):
    md_api_key : str
    name : str
    data_store : str
    input_type : InputTypeEnum
    input_filter : str
    input_keys : str
    ingest_type : IngestTypeEnum
    ingest_params : str
    timer_interval : int
    timer_on : int

class IngestPipelineRunMessage(BaseModel):
    md_api_key : str
    data_store : str
    name : str


###############################################################################
# Query Pipeline                                                              #
###############################################################################

class QueryTypeEnum(IntEnum):
    Text = 1
    Image = 2
    SQL = 3

class QueryModeEnum(IntEnum):
    Refine = 1
    Compact = 2
    Accumulate = 3

class QueryPipeline(BaseModel):
    id : str
    group : str
    workspace : str
    user_name :  str
    name : str
    data_store : str
    query_type : QueryTypeEnum
    llm_model : str
    query_params : str

class QueryPipelineMessage(BaseModel):
    user_token : str
    name : str
    data_store : str
    query_type : QueryTypeEnum
    llm_model : str
    query_params : str
