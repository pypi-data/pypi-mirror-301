"""Import device types and module types from our repository .yaml definitions to Nautobot"""
from argparse import Namespace
import os
from pprint import pprint
import requests
import yaml
from pynautobot.core.api import Api
from pynautobot.models.dcim import Record
from py_populate_dcim_lib.fetchers.nautobot.nautobot_helpers import fetch_nautobot_form_content, fetch_nautobot_sessionid


def create_nautobot_device_manufacturer(nautobot: Api, manufacturer: str):
    """
    Creates a Manufacturer in Nautobot
    given the Manufacturer name
    """
    search_manufacturer: list[Record] = nautobot.dcim.manufacturers.filter(name=manufacturer)
    if search_manufacturer:
        # print("DEBUG: Not creating a new manufacturer in Nautobot since it already exists: ", manufacturer)
        pass
    else:
        # build our request metadata
        nautobot.http_session.cookies.clear()

        # build our request data
        body = {
            "name": manufacturer
        }
        print("INFO: Creating a new manufacturer in Nautobot", manufacturer)
        nautobot.dcim.manufacturers.create(body)
        # clear cookies now that they've been used
        nautobot.http_session.cookies.clear()


def list_files_walk(start_path='.') -> list[str]:
    file_list: list[str] = []
    for root, dirs, files in os.walk(start_path):
        for file in files:
            # print(os.path.join(root, file))
            file_list.append(os.path.join(root, file))

    return file_list


def import_new_nautobot_types(nautobot: Api) -> list[requests.Response]:
    '''
    Imports all Nautobot types that
    DO NOT EXIST YET
    '''
    types_path = os.environ.get(
        'NAUTOBOT_TYPES_PATH', 'nautobot-types/')
    print("DEBUG: Searching for Device and Module types in", types_path)

    file_list = list_files_walk(types_path)

    if len(file_list) <= 0:
        print("WARN: No resources were found to add Device Types or Module Types to Nautobot")

    for file in file_list:
        filename = os.fsdecode(file)
        if filename.endswith(".yaml") or filename.endswith(".yml"):
            with open(filename, encoding='utf-8') as data:
                yaml_data: dict = yaml.safe_load(data)
                type_model: str = yaml_data.get("model")
                manufacturer: str = yaml_data.get("manufacturer")

                # assure that Nautobot knows about this manufacturer
                create_nautobot_device_manufacturer(nautobot, manufacturer)

                if "module-types" in filename:
                    module_model_search: list = nautobot.dcim.module_types.filter(model=type_model)
                    if module_model_search:
                        print("DEBUG: Skipping Module Type creation because a type with its model exists: ", type_model)
                        continue

                    ## build new object to represent new connection
                    # build metadata
                    dbg_headers = {
                        "Content-Type": "application/x-www-form-urlencoded;",
                        "Authorization": f"Token {nautobot.token}",
                    }
                    (csrf_token, csrf_middleware_token) = fetch_nautobot_form_content(nautobot, nautobot.base_url.replace("/api", "")+ "/dcim/devices/", "csrfmiddlewaretoken")
                    nautobot.http_session.cookies.set("csrftoken", csrf_token)
                    session_id = fetch_nautobot_sessionid(nautobot, csrf_middleware_token)
                    nautobot.http_session.cookies.set("sessionid", session_id)
                    # build our request data
                    body: dict = {
                        "csrfmiddlewaretoken": csrf_middleware_token,
                        "data": yaml.dump(yaml_data),
                        "format": "yaml",
                        "_create": "",
                    }
                    post_res = requests.post(nautobot.base_url.replace("/api", "") + "/dcim/module-types/import/", \
                        data=body, cookies=nautobot.http_session.cookies, headers=dbg_headers, timeout=5)



                    # send the request to Nautobot to create the new connection
                    # nautobot.dcim.module_types.create(body)

                    # clear cookies now that they've been used
                    nautobot.http_session.cookies.clear()
                    # results.append((post_res, port.get("mac")))


                elif "device-types" in filename:
                    device_model_search: list[Record] = nautobot.dcim.device_types.filter(model=type_model)
                    if device_model_search:
                        print("DEBUG: Skipping Device Type creation because a type with its model exists: ", type_model)
                        update_existing_nautobot_types(nautobot, "device", device_model_search)
                        continue

                    ## build new object to represent new connection
                    # build metadata
                    dbg_headers = {
                        "Content-Type": "application/x-www-form-urlencoded;",
                        "Authorization": f"Token {nautobot.token}",
                    }
                    (csrf_token, csrf_middleware_token) = fetch_nautobot_form_content(nautobot, nautobot.base_url.replace("/api", "")+ "/dcim/devices/", "csrfmiddlewaretoken")
                    nautobot.http_session.cookies.set("csrftoken", csrf_token)
                    session_id = fetch_nautobot_sessionid(nautobot, csrf_middleware_token)
                    nautobot.http_session.cookies.set("sessionid", session_id)
                    # build our request data
                    body: dict = {
                        "csrfmiddlewaretoken": csrf_middleware_token,
                        "data": yaml.dump(yaml_data),
                        "format": "yaml",
                        "_create": "",
                    }
                    post_res = requests.post(nautobot.base_url.replace("/api", "") + "/dcim/device-types/import/", \
                        data=body, cookies=nautobot.http_session.cookies, headers=dbg_headers, timeout=5)
                    # clear cookies now that they've been used
                    nautobot.http_session.cookies.clear()
                    # results.append((post_res, port.get("mac")))

    return


def update_existing_nautobot_types(nautobot: Api, device_or_module: str, searched_type: list[Record]):
    '''
    TODO: complete a diff and update existing Device Types and Module Types
    Updates existing Nautobot types that already exist.
    This keeps the old types to not delete associated devices.
    '''
    if device_or_module == "device":
        pass
        # print("found existing type")
        # pprint(dict(searched_type[0]))
        
        # diff the existing device's contents (Interfaces, Module Bays, Power Ports, Console Ports, Comments, etc) and add/delete contents according to diff
        
        # to delete an interface
        # post http://localhost:8080/dcim/interface-templates/7e2e3279-9941-4843-ae41-2a12c216e891/delete/?return_url=/dcim/device-types/86ca7588-487c-410c-b72e-4a8b2af2600e/?tab=interfaces
        # with request body 'confirm': True
        
        # to add a module bay
        # get http://localhost:8080/dcim/module-bay-templates/add/?device_type=86ca7588-487c-410c-b72e-4a8b2af2600e&return_url=/dcim/device-types/86ca7588-487c-410c-b72e-4a8b2af2600e/?tab=modulebays
        # post http://localhost:8080/dcim/module-bay-templates/add/?device_type=86ca7588-487c-410c-b72e-4a8b2af2600e&return_url=/dcim/device-types/86ca7588-487c-410c-b72e-4a8b2af2600e/?tab=modulebays
        # with body contents
        # 'device_type': searched_type.id
        # 'name_pattern': module bay name
        # 'position_pattern': module bay position-
    elif device_or_module == "module":
        pass
    return
