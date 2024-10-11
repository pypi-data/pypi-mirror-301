import random
import string
import sys
import os
import json
import logging
from pathlib import Path
import requests
from hpOneView.oneview_client import OneViewClient
from dotenv import load_dotenv


log = logging.getLogger(__name__)

def enable_netop() -> dict:
    '''
    automates the enabling of read-only cli access for OneView Synergy Switches
    returns a dict of domain names and randomly-generated passwords
    '''
    # connect to OneView API
    print("INFO: Connecting to OneView...")
    # NOTE: to use this script, set the ONEVIEWSDK_IP environment variable to the GLOBAL OneView applicance
    global_oneview_client = OneViewClient.from_environment_variables()
    print("INFO: Connected to OneView!")


    # fetch all interconnect URIs
    interconnects: list[dict] = global_oneview_client.interconnects.get_all()
    metadata = {}
    accepted_models = [
        "Virtual Connect SE 40Gb F8 Module for Synergy",
        "Virtual Connect SE 100Gb F32 Module for Synergy"
    ]
    for interconnect in interconnects:
        if any(model in interconnect.get("productName") for model in accepted_models):
            # build a query to reset netop password for each device
            appliance_config = {
                "ip": interconnect.get("applianceLocation"),
                "credentials": {
                    "userName": os.environ.get('ONEVIEWSDK_USERNAME', ''),
                    "password": os.environ.get('ONEVIEWSDK_PASSWORD', ''),
                    "authLoginDomain": "LOCAL"
                }
            }
            appliance_oneview_client = OneViewClient(appliance_config)
            headers = {
                "Content-Type": "application/json",
                "X-API-Version": "5600",
                "auth": appliance_oneview_client.connection.get_session_id(),
            }
            new_secret = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(31))
            patch_request_body = json.dumps([{"op":"replace","path":"/netOpPasswd","value": new_secret}])
            req_link = "https://" + interconnect.get("applianceLocation") + interconnect.get("originalUri")
            # print("! Updating netop password for resource at:", req_link)
            # print(json.dumps(interconnect, sort_keys=True, indent=4))
            res = requests.patch(req_link, patch_request_body, headers=headers, verify=False)
            # TODO: handle errors from API calls
            # print(res)
            metadata_entry = {}
            metadata_entry["applianceLocation"] = interconnect.get("applianceLocation")
            metadata_entry["bayNumber"] = interconnect.get("bayNumber")
            metadata_entry["enclosureName"] = interconnect.get("enclosureName")
            metadata_entry["secret"] = new_secret
            metadata[interconnect.get("originalUri")] = metadata_entry
        else:
            print("product differs from accepted_models             ", interconnect)
    print(json.dumps(metadata, sort_keys=True, indent=4))
    return metadata

# assure the user has provided a .env file
if not Path(".env").is_file():
    sys.exit("ERROR: you must provide a .env file")
else:
    load_dotenv()

enable_netop()
