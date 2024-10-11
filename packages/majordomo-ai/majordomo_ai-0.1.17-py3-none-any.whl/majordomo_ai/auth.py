from enum import Enum, IntEnum
from pydantic import BaseModel
import os
import json

class Credentials(BaseModel):
    account_id : int
    workspace : str | None = ""
    md_api_key : str | None = ""
    extra_tags : str | None = ""

def MdSuccessResponse(success):
    response = {}
    if success != '':
        response['response'] = success
    response['status'] = 0

    return json.dumps(response)

def MdErrorResponse(error):
    response = {}
    response['status'] = -1
    response['error'] = error

    return json.dumps(response)

def CreateCredentials():

    json_input = {}

    if os.getenv("MAJORDOMO_AI_ACCOUNT") is None:
        raise Exception("Environment variable MAJORDOMO_AI_ACCOUNT not set")
    json_input["account_id"] = int(os.getenv("MAJORDOMO_AI_ACCOUNT"))

    if os.getenv("MAJORDOMO_AI_WORKSPACE") is None:
        raise Exception("Environment variable MAJORDOMO_AI_WORKSPACE not set")
    json_input["workspace"] = os.getenv("MAJORDOMO_AI_WORKSPACE")

    if os.getenv("MAJORDOMO_AI_API_KEY") is None:
        raise Exception("Environment variable MAJORDOMO_AI_API_KEY not set")
    json_input["md_api_key"] = os.getenv("MAJORDOMO_AI_API_KEY")

    return json_input

def CreateCredentialsWith(account, workspace, md_api_key):

    json_input = {}

    json_input["account_id"] = int(account)
    json_input["workspace"] = workspace
    json_input["md_api_key"] = md_api_key

    return json_input
