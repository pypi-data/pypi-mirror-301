import json
import pickle
import re
from pynautobot.core.api import Api
from pynautobot.models.dcim import Devices, Interfaces, Record
import requests
from ...fetchers.helpers import xstr
from ...fetchers.nautobot.nautobot_helpers import fetch_nautobot_form_content, fetch_nautobot_generic, fetch_nautobot_sessionid
from hpeOneView.resources.servers.server_hardware import ServerHardware
from requests_toolbelt import MultipartEncoder

# Virtual Connect device parent bays (for children devices like OneView Virtual Connects)
def fetch_nautobot_vc_dict(nautobot: Api, match_name: str, parent_devices: Devices) -> dict[dict]:
    '''
    parent_devices: list of SYNFRAME devices available in nautobot that each contain device bays.
                    one of these device bays is our expressed Virtual Connect Module
    match_name: a set of strings (or single string) that our Virtual Connects are named in Nautobot
    returns a nested dictionary of all of our devices
    '''
    nautobot_oneview_vc_devices: list[Devices] = nautobot.dcim.devices.filter(name__ic=match_name)
    ## create a dict relating one Virtual Connect device per SYNFRAME in Nautobot
    nautobot_frame_vc = {}
    for vc_device in nautobot_oneview_vc_devices:
        # print(json.dumps(vc_device.serialize(), indent=4))
        vc_device_metadata = {}
        if vc_device.parent_bay and vc_device.parent_bay.url:
            device_parent_bay: dict = fetch_nautobot_generic(nautobot, vc_device.parent_bay.url)
        else:
            print("WARN: Virtual Connect device ", vc_device, " does not have a parent attribute")
        vc_device_metadata["parent_bay"] = device_parent_bay
        vc_device_metadata["device"] = vc_device.serialize()
        vc_device_metadata["parent"] = next((parent.serialize() for parent in parent_devices if parent['id'] == device_parent_bay.get("device").get("id")), None)
        nautobot_frame_vc[vc_device.id] = vc_device_metadata
    return nautobot_frame_vc

# construct a list of SYNFRAME devices missing a corresponding child Virtual Connect device
def find_frames_missing_vc_devices(vc_devices: dict, frame_devices: list[Devices]) -> list[Devices]:
    '''
    Given a list of Virtual Connect devices and Synergy Frame devices,
    return a list of Synergy Frame devices that do not have associated Virtual Connect devices
    '''
    for vc in vc_devices:
        vc_parent_id = vc_devices[vc].get("parent").get("id")
        for index, frame in enumerate(frame_devices):
            if frame.id == vc_parent_id:
                frame_devices.pop(index)
    return frame_devices


def create_missing_vc_devices(nautobot: Api, frames_without_vcs: list[Devices], oneview_frame_models: set | dict, aci_oneview_pairs: dict) -> tuple:
    '''
    Given a list of Synergy Frame devices that do not have associated Virtual Connects,
    create the new Virtual Connect devices and try to add their association to their corresponding Frame
    '''

    # only process Virtual Connects if find_frames_missing_vc_devices() deemed devices missing
    # else, do nothing
    if len(frames_without_vcs) == 0:
        return (None, None)
    else:
        create_virtual_connect_role(nautobot)
        # this object stores the outcome of VC device creation / lookup
        new_vc_devices_result: list = []
        # build objects for new Virtual Connect devices    
        new_devices: list[dict] = []
        oneview_frame_models = dict(oneview_frame_models)
        for lone_frame in frames_without_vcs:
            lone_frame_data = lone_frame.serialize()
            vc_device_type: str = oneview_frame_models.get(lone_frame.name)

            # discover bay from aci_oneview_pairs
            bay = None
            for pair in aci_oneview_pairs:
                # for source in aci_oneview_pairs[pair]:
                if aci_oneview_pairs[pair]["oneView"].get("frame") == lone_frame.name:
                    port_loc: str = aci_oneview_pairs[pair]["oneView"]["portLoc"]
                    if port_loc.startswith("1"):
                        bay = 6
                        break
                    elif port_loc.startswith("0"):
                        bay = 3
                        break
                        
            new_name = "Virtual Connect Bay " + str(bay) + " for " + lone_frame.name
            
            # find Interconnect Bay <bay> id for lone_frame
            bay_filters = {
                "name": "Interconnect Bay " + str(bay),
                "device": lone_frame_data.get('id')
            }
            interconnect_bay_search_url = nautobot.base_url + "/dcim/device-bays/"
            vc_interconnect_bay = fetch_nautobot_generic(nautobot, interconnect_bay_search_url, bay_filters)[0]
            
            # make sure that we are not trying to duplicate the Virtual Connect device
            lookup_device: list[Devices] = nautobot.dcim.devices.filter(name__ie=new_name)
            if len(lookup_device) != 0:
                print("DEBUG: Found a VC device", new_name, "- skipping creation of this device")
                lookup_device_data = lookup_device[0].serialize()
                lookup_device_data['parent_bay'] = vc_interconnect_bay.get("id")
                new_vc_devices_result.append(lookup_device_data)
                continue

            new_vc_device = {
                "name": new_name,
                "device_type": {"model": vc_device_type},
                "status": {
                    "name": "Active",
                },
                "role": {"name": "Synergy Virtual Connect"},
                "location": lone_frame_data.get("location"),
                "rack": lone_frame_data.get("rack"),
                "parent_bay": vc_interconnect_bay.get("id"),
            }
            new_devices.append(new_vc_device)
        
        # actually create the new devices that do not exist
        if new_devices:
            print("DEBUG: creating the following Virtual Connect devices:", json.dumps(new_devices, indent=4))
            if len(nautobot.http_session.cookies.keys()) > 0:
                print("DEBUG: removing stale nautobot Api cookies")
                nautobot.http_session.cookies.clear()
            new_devices_results = nautobot.dcim.devices.create(new_devices)
            
            for result in new_devices_results:
                new_vc_devices_result.append(result)
        
        # populate the new device parents in a device bay
        new_vc_children_result = []
        for new_vc in new_vc_devices_result:
            new_device_child = populate_frame_device_bay(nautobot, new_vc)
            new_vc_children_result.append(new_device_child)
        return (new_vc_devices_result, new_vc_children_result)

def create_virtual_connect_role(nautobot: Api):

    nautobot.http_session.cookies.clear()
    csrf_middleware_token: str
    (csrf_token, csrf_middleware_token) = fetch_nautobot_form_content(nautobot, nautobot.base_url.replace("/api", "") + "/dcim/locations/", "csrfmiddlewaretoken")
    nautobot.http_session.cookies.set("csrftoken", csrf_token)
    session_id = fetch_nautobot_sessionid(nautobot, csrf_middleware_token)
    nautobot.http_session.cookies.set("sessionid", session_id)

    body = MultipartEncoder(
        fields = {
        "csrfmiddlewaretoken": csrf_middleware_token,
        "name": "Synergy Virtual Connect",
        "description": "Virtual Connect Switches for HPE Synergy Frames",
        "content_types": "3", # dcim | device,
        "color": "f44336"
    })

    hederz = {
        "Content-Type": body.content_type,
    }
    post_res: requests.Response =  requests.post(nautobot.base_url.replace("/api", "") + "/extras/roles/add/", \
        data=body, cookies=nautobot.http_session.cookies, headers=hederz, timeout=5)
    # clear cookies now that they've been used
    nautobot.http_session.cookies.clear()

    return post_res

def populate_frame_device_bay(nautobot: Api, new_vc_device: Devices | dict):
    '''
    Write to nautobot to associate an existing Virtual Connect device to its corresponding Synergy Frame device
    '''
    if type(new_vc_device) != dict:
        new_vc_device = new_vc_device.serialize()
    print("DEBUG: Associating device: ", new_vc_device.get("name"), "with parent device bay")
    dbg_headers = {
        "Content-Type": "application/x-www-form-urlencoded;",
        "Authorization": f"Token {nautobot.token}",
    }
    (csrf_token, csrf_middleware_token) = fetch_nautobot_form_content(nautobot, nautobot.base_url.replace("/api", "")+ "/dcim/device-bays/" + xstr(new_vc_device.get("parent_bay")), "csrfmiddlewaretoken")
    nautobot.http_session.cookies.set("csrftoken", csrf_token)
    session_id = fetch_nautobot_sessionid(nautobot, csrf_middleware_token)
    nautobot.http_session.cookies.set("sessionid", session_id)
    body: dict = {
        "installed_device": new_vc_device.get("id"),
        "csrfmiddlewaretoken": csrf_middleware_token,
        "_update": ""
    }
    post_res = requests.post(nautobot.base_url.replace("/api", "") + "/dcim/device-bays/" + xstr(new_vc_device.get("parent_bay")) + "/populate/", \
        data=body, cookies=nautobot.http_session.cookies, headers=dbg_headers, timeout=5)
    # clear cookies now that they've been used
    nautobot.http_session.cookies.clear()
    return post_res


## interfaces
def fetch_nautobot_device_interfaces(nautobot: Api, devices: list[Devices]) -> tuple[dict[list[Interfaces]]]:
    '''
    from a list of devices,
    provide a tuple
    each entry contains a dictionary with lists of interfaces
    seperated by rear bay slot
    '''
    nautobot_bay3_interfaces: dict[list[Interfaces]] = {}
    nautobot_bay6_interfaces: dict[list[Interfaces]] = {}
    for device in devices:
        if "Bay 3" in device.name:
            device_bay3_interfaces: list[Interfaces] = nautobot.dcim.interfaces.filter(device=device.id)
            nautobot_bay3_interfaces[device.id] = device_bay3_interfaces
        if "Bay 6" in device.name:
            device_bay6_interfaces: list[Interfaces] = nautobot.dcim.interfaces.filter(device=device.id)
            nautobot_bay6_interfaces[device.id] = device_bay6_interfaces

    return nautobot_bay3_interfaces, nautobot_bay6_interfaces


def create_missing_vc_interfaces(nautobot: Api, device_pairs: dict, ) -> requests.Response:
    '''
    given a list of all device_pairs
    search for interface links
    and create the missing interface links
    '''
    for new_connection in device_pairs:
        ## find oneview frame (parent) device
        oneview_frame_name: str = device_pairs[new_connection].get("oneView").get("frame")
        # oneview_frame_device = nautobot.dcim.devices.filter(name__ie=oneview_frame_name)

        ## find oneview Virtual Connect device
        oneview_port_loc = device_pairs[new_connection].get("oneView").get("portLoc")
        bay = None
        if re.match("(^0\\/)", oneview_port_loc):
            bay = 3
        elif re.match("(^1\\/)", oneview_port_loc):
            bay = 6
        oneview_vc_device = nautobot.dcim.devices.filter(name__ie="Virtual Connect Bay " + str(bay) + " for " + oneview_frame_name)

        ## find oneview Virtual Connect interface
        q_port_num = re.search("([0-9]:[0-9]$)", oneview_port_loc)
        oneview_vc_interfaces = nautobot.dcim.interfaces.filter(device=oneview_vc_device, name__iew=q_port_num.group(0))
        if len(oneview_vc_interfaces) > 0:
            oneview_vc_interface = oneview_vc_interfaces[0]
        else:
            oneview_vc_interface = None
            print("WARN: Skipping interface creation because a Synergy Frame named", oneview_frame_name, "does not exist")
            post_res = None
            continue

        ## don't create the connected_endpoint if one already exists
        if oneview_vc_interface.connected_endpoint:
            # print("DEBUG: not creating a new interface link because one is already populated for " + oneview_vc_interface.name + "on frame" + oneview_frame_name)
            post_res = None
            continue

        ## find aci leaf device
        aci_leaf_name = device_pairs[new_connection].get("aci").get("nodeName")
        aci_leaf_device = nautobot.dcim.devices.filter(name__ie=aci_leaf_name)[0]
        # print("aci_leaf_device", json.dumps(aci_leaf_device.serialize(), indent=4))
        ## find aci leaf device interface
        aci_port_num = re.search("([0-9]\\/[0-9]*.$)", device_pairs[new_connection]["aci"]["portLoc"])
        aci_leaf_interface = nautobot.dcim.interfaces.filter(device=aci_leaf_device.id, name__iew=aci_port_num.group(0))[0]

        print("DEBUG: connecting OneView and ACI endpoints", oneview_frame_name, aci_leaf_name)
        ## build new object to represent new connection
        dbg_headers = {
            "Content-Type": "application/x-www-form-urlencoded;",
            "Authorization": f"Token {nautobot.token}",
        }

        connected_status = nautobot.extras.statuses.filter(name__ie="Connected")[0]

        (csrf_token, csrf_middleware_token) = fetch_nautobot_form_content(nautobot, nautobot.base_url.replace("/api", "")+ "/dcim/interfaces/" + xstr(oneview_vc_interface.id), "csrfmiddlewaretoken")
        nautobot.http_session.cookies.set("csrftoken", csrf_token)
        session_id = fetch_nautobot_sessionid(nautobot, csrf_middleware_token)
        nautobot.http_session.cookies.set("sessionid", session_id)
        body: dict = {
            "csrfmiddlewaretoken": csrf_middleware_token,
            "_update": "",
            "termination_b_location": aci_leaf_device.location.id, #re.search("([^\\/]+$)", str(aci_leaf_device.location.id).removesuffix("/")).group(0),
            "termination_b_rack": aci_leaf_device.rack.id, #re.search("([^\\/]+$)", str(aci_leaf_device.rack.id).removesuffix("/")).group(0),
            "termination_b_device": aci_leaf_device.id,
            "termination_b_id": aci_leaf_interface.id,
            "status": connected_status.id
        }
        post_res = requests.post(nautobot.base_url.replace("/api", "") + "/dcim/interfaces/" + xstr(oneview_vc_interface.id) + "/connect/interface/", \
            data=body, cookies=nautobot.http_session.cookies, headers=dbg_headers, timeout=5)
        # clear cookies now that they've been used
        nautobot.http_session.cookies.clear()
    return post_res
