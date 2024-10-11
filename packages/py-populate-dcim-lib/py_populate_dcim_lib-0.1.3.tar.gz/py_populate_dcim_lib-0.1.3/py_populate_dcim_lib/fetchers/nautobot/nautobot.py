"""Module providing interfaces to Nautobot, Cisco ACI APIC, and HPE Oneview for DCIM population"""

import json
from pynautobot.core.api import Api
from pynautobot.models.dcim import Devices, Record
import requests
from ...fetchers.helpers import xstr
from ...fetchers.nautobot.nautobot_helpers import fetch_nautobot_form_content, fetch_nautobot_generic, fetch_nautobot_sessionid
from hpeOneView.resources.servers.server_hardware import ServerHardware
from requests_toolbelt import MultipartEncoder

# ACI devices


def fetch_check_nautobot_devices_vs_aci(nautobot: Api, match_names: list[str], aci_node_names: set[str]) -> list[Devices]:
    '''
    Poll Nautobot for its devices and compare to a list of devices from ACI
    returns a list of Devices that match ACI node names
    '''
    nautobot_leaf_devices: Devices = nautobot.dcim.devices.filter(
        name__ic=match_names)
    for aci_node in aci_node_names:
        if aci_node.upper() not in (leaf_device.name.upper() for leaf_device in nautobot_leaf_devices):
            # TODO: add all missing switches to nautobot
            print("WARN: An ACI device named", aci_node,
                  "has not been accounted for in nautobot and will be ignored for now")
    return nautobot_leaf_devices


# OneView Devices
def fetch_check_nautobot_frames_vs_oneview(nautobot: Api, match_names: list[str], oneview_node_names: set) -> list[Devices]:
    '''
    Poll Nautobot for its devices and compare to a list of devices from OneView
    '''
    nautobot_leaf_devices: Devices = nautobot.dcim.devices.filter(
        name__ie=match_names)
    for oneview_node in oneview_node_names:
        if oneview_node.upper() not in (leaf_device.name.upper() for leaf_device in nautobot_leaf_devices):
            # TODO: add all missing switches to nautobot
            print("WARN: A OneView device named", oneview_node,
                  "has not been accounted for in nautobot and will be ignored for now")
    return nautobot_leaf_devices


def create_unknown_location(nautobot: Api):
    '''
    When created via API, new devices require a "location" be set.
    However, the API client does not know the location of these objects,
    so we create a placeholder "Unknown" location :)
    '''

    active_status: str = nautobot.extras.statuses.filter(name__ie="Active")[
        0].id
    create_unknown_location_type(nautobot)
    location_type: str = nautobot.dcim.location_types.filter(name__ie="Unknown")[
        0].id

    nautobot.http_session.cookies.clear()
    csrf_middleware_token: str
    (csrf_token, csrf_middleware_token) = fetch_nautobot_form_content(nautobot,
                                                                      nautobot.base_url.replace("/api", "") + "/dcim/locations/add/", "csrfmiddlewaretoken")
    nautobot.http_session.cookies.set("csrftoken", csrf_token)
    session_id = fetch_nautobot_sessionid(nautobot, csrf_middleware_token)
    nautobot.http_session.cookies.set("sessionid", session_id)

    body = MultipartEncoder(
        fields={
            "csrfmiddlewaretoken": csrf_middleware_token,
            "location_type": location_type,
            "name": "Unknown",
            "description": "A placeholder location for devices added via API",
            "status": active_status
        })

    hederz = {
        "Content-Type": body.content_type,
    }
    post_res: requests.Response = requests.post(nautobot.base_url.replace("/api", "") + "/dcim/locations/add/",
                                                data=body, cookies=nautobot.http_session.cookies, headers=hederz, timeout=5)
    # clear cookies now that they've been used
    nautobot.http_session.cookies.clear()

    return post_res


def create_unknown_location_type(nautobot: Api):

    nautobot.http_session.cookies.clear()
    csrf_middleware_token: str
    (csrf_token, csrf_middleware_token) = fetch_nautobot_form_content(nautobot,
                                                                      nautobot.base_url.replace("/api", "") + "/dcim/location-types/add/", "csrfmiddlewaretoken")
    nautobot.http_session.cookies.set("csrftoken", csrf_token)
    session_id = fetch_nautobot_sessionid(nautobot, csrf_middleware_token)
    nautobot.http_session.cookies.set("sessionid", session_id)

    body = MultipartEncoder(
        fields={
            "csrfmiddlewaretoken": csrf_middleware_token,
            "name": "Unknown",
            "description": "A placeholder location for devices added via API",
            "content_types": "3"  # dcim | device
        })

    hederz = {
        "Content-Type": body.content_type,
    }
    post_res: requests.Response = requests.post(nautobot.base_url.replace("/api", "") + "/dcim/location-types/add/",
                                                data=body, cookies=nautobot.http_session.cookies, headers=hederz, timeout=5)
    # clear cookies now that they've been used
    nautobot.http_session.cookies.clear()

    return post_res
