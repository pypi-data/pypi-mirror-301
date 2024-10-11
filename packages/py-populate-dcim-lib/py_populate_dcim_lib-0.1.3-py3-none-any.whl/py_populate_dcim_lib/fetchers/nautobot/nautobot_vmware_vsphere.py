
"""Creates Devices, Modules, and interface connections for OneView rack-mounted devices"""
import json
import re
from etherflow_acitoolkit.acisession import Session
from ...fetchers.aci.aci_port_channel import PortChannelCollector
from ...fetchers.aci.aci_ip_endpoints import IpEndpointCollector
from pynautobot.core.api import Api
from pynautobot.models.dcim import Record
from hpeOneView.resources.servers.server_hardware import ServerHardware
import requests
from requests_toolbelt import MultipartEncoder

from ...fetchers.helpers import xstr
from ...fetchers.nautobot.nautobot_helpers import fetch_nautobot_form_content, fetch_nautobot_sessionid
from ...fetchers.nautobot.nautobot import create_unknown_location


def create_oneview_server_modules(nautobot: Api, oneview_servers: list[ServerHardware]) -> requests.Response:

    def build_module_object(server_id: str, position: str, module_type_id: str, status_active_id: str, slot: str | None = None) -> dict[str]:
        new_nautobot_module = {}

        # locate module bay
        search_device_bay: list[Record] = nautobot.dcim.module_bays.filter(
            parent_device=server_id, position=position)
        if len(search_device_bay) != 0:
            device_bay_id: str = search_device_bay[0].id
        elif slot:
            # if no OCP device is found with initial search, try searching in module slots
            search_device_bay: list[Record] = nautobot.dcim.module_bays.filter(
                parent_device=server_id, position=position + "-" + slot)
            device_bay_id: str = search_device_bay[0].id

        # assure we are not re-creating this module
        module_search: list[Record] = nautobot.dcim.modules.filter(
            parent_module_bay=device_bay_id)
        if len(module_search) != 0:
            return
        new_nautobot_module = {
            "module_type": module_type_id,
            "status": status_active_id,
            "parent_module_bay_device_filter": server_id,  # parent device
            "parent_module_bay": device_bay_id  # parent device module bay
        }
        return new_nautobot_module

    new_modules: list[dict] = []
    new_modules_result: list = []
    status_active_id: str = nautobot.extras.statuses.filter(name__ie="Active")[
        0].id
    for server in oneview_servers:
        if "portMap" in server:
            server_search: list[Record] = nautobot.dcim.devices.filter(
                name__ie=re.sub("(ilo)(?=$|[.\n]{1})", "", server.get("name")))
            server_id: str = server_search[0].id
            if server.get("portMap"):
                for module_slot in server.get("portMap"):
                    for nic in server.get("portMap")[module_slot]:
                        module_name: str = nic.get("deviceName")

                        location: str = nic.get("location").lower()
                        if location != "lom":
                            search_module_type_id: str = nautobot.dcim.module_types.filter(
                                comments__ic=module_name)[0].id
                        else:
                            # lights out module (integrated to server motherboard)
                            pass

                        if location == "flr":
                            # FlexLOM
                            new_nautobot_module = build_module_object(
                                server_id, "FlexLOM", search_module_type_id, status_active_id)
                            if new_nautobot_module:
                                new_modules.append(new_nautobot_module)

                        if location == "ocp":
                            # OCP
                            new_nautobot_module = build_module_object(
                                server_id, "OCP3", search_module_type_id, status_active_id, str(nic.get("slotNumber")))
                            if new_nautobot_module:
                                new_modules.append(new_nautobot_module)

                        if location == "pci":
                            # PCIe
                            pcie_slot_number: str = str(nic.get("slotNumber"))
                            new_nautobot_module = build_module_object(
                                server_id, "PCIe" + pcie_slot_number, search_module_type_id, status_active_id)
                            if new_nautobot_module:
                                new_modules.append(new_nautobot_module)

    if len(new_modules) > 0:
        print("DEBUG: creating the following Virtual Connect devices:",
              json.dumps(new_modules, indent=4))
        if len(nautobot.http_session.cookies.keys()) > 0:
            print("DEBUG: removing stale nautobot Api cookies")
            nautobot.http_session.cookies.clear()
        new_devices_results = nautobot.dcim.modules.create(new_modules)

        for result in new_devices_results:
            new_modules_result.append(result)
    return new_modules_result


def create_oneview_server_devices(nautobot: Api, oneview_servers: list[ServerHardware]):

    create_unknown_location(nautobot)
    create_server_role(nautobot)

    new_devices_result: list = []
    new_devices: list[dict] = []

    role_id: str = nautobot.extras.roles.filter(name__ie="Server")[0].id
    loc_unknown_id: str = nautobot.dcim.locations.filter(name__ie="Unknown")[
        0].id
    status_active_id: str = nautobot.extras.statuses.filter(name__ie="Active")[
        0].id

    for server in oneview_servers:
        # assure we are not re-creating this device
        device_search: list[Record] = nautobot.dcim.devices.filter(
            name__ie=re.sub("(ilo)(?=$|[.\n]{1})", "", server.get("name")))
        if len(device_search) != 0:
            continue

        new_nautobot_device = {
            "name": re.sub("(ilo)(?=$|[.\n]{1})", "", server.get("name")),
            "role": role_id,
            "device_type": {"model": server.get("model")},
            "serial": server.get("serialNumber"),
            "location": loc_unknown_id,
            "status": status_active_id
        }
        new_devices.append(new_nautobot_device)

    # actually create the new devices that do not exist
    if new_devices:
        print("DEBUG: creating ", len(new_devices),
              " HPE Server devices:", json.dumps(new_devices, indent=4))
        if len(nautobot.http_session.cookies.keys()) > 0:
            print("DEBUG: removing stale nautobot Api cookies")
            nautobot.http_session.cookies.clear()
        new_devices_results = nautobot.dcim.devices.create(new_devices)

        for result in new_devices_results:
            new_devices_result.append(result)

    return new_devices_result


def create_interfaces(nautobot: Api, server_id: str, nic: dict, position: str, connected_status: str, filtered_aci_infos: dict, aci_node_names: dict):
    """
    Create Ethernet connections between OneView racked servers and their Cisco switches.
    This function handles OneView hardware with modular NICs as well as integrated ports.
    This function DOES NOT include iLO interfaces.
    :nic: a dictionary describing the modular network interface card looked up in nautobot
    :position: a string that describes a module's installation location (lom, ocp, pci, etc.)
    """

    module_interfaces_results: list[tuple[requests.Response, str]] = []

    if position:  # if slot position is given, this is interface sits on a module
        # find NIC module
        module_bay_search = nautobot.dcim.module_bays.filter(
            parent_device=server_id, position=position)

        if len(module_bay_search) != 0:
            device_module_bay_id: str = module_bay_search[0].id
        else:
            # if no OCP device is found with initial search, try searching in module slot
            position = position + "-" + \
                str(nic.get("slotNumber"))
            search_device_bay: list[Record] = nautobot.dcim.module_bays.filter(
                parent_device=server_id, position=position)
            device_module_bay_id: str = search_device_bay[0].id

        module_search = nautobot.dcim.modules.filter(
            parent_module_bay=device_module_bay_id)
        module_id = module_search[0].id

    for port in nic.get("physicalPorts"):
        # find single interface inside of NIC module
        if position:
            interface_search = nautobot.dcim.interfaces.filter(
                module=module_id, name__ic=str(port.get("portNumber")))
            interface_id = interface_search[0].id
        # or if no NIC module position is provided, it is a device port
        else:
            interface_search = nautobot.dcim.interfaces.filter(
                device=server_id, module__isnull=True, name__ic=str(port.get("portNumber")))
            interface_id = interface_search[0].id

        # assure we don't recreate this interface
        # if interface is already populated, skip it
        if interface_search[0].connected_endpoint:
            print(
                "DEBUG: Skipping HPE rack-mount interface connection creation because one already exists", interface_search[0].connected_endpoint)
            continue

        aci_port_data = filtered_aci_infos.get(
            port.get("mac"))

        if aci_port_data:
            port_interface_name = aci_port_data.get(
                "if_name")
            node_id = re.search(
                "(?<=eth [0-9]{1}/)([0-9]{3})(?=/)", port_interface_name)
            port_number = re.search(
                "([0-9]/[0-9]{1,3})(?:\n|$)", port_interface_name)
            if node_id:
                node_name = aci_node_names[node_id.group(
                    0)]
                aci_device = nautobot.dcim.devices.filter(
                    name__ie=node_name)
                if not aci_device:
                    print("ERROR: Found no matching ACI leaf device in Nautobot named: ",
                          node_name, " when creating network interface connections.")
                    continue
                else:
                    aci_device = aci_device[0]

                aci_leaf_interface = nautobot.dcim.interfaces.filter(
                    device=aci_device.id, name__iew=port_number.group(0))[0]

                # build our request metadata
                nautobot.http_session.cookies.clear()
                csrf_middleware_token: str
                (csrf_token, csrf_middleware_token) = fetch_nautobot_form_content(
                    nautobot, nautobot.base_url.replace("/api", "") + "/dcim/locations/", "csrfmiddlewaretoken")
                nautobot.http_session.cookies.set(
                    "csrftoken", csrf_token)
                session_id = fetch_nautobot_sessionid(
                    nautobot, csrf_middleware_token)
                nautobot.http_session.cookies.set(
                    "sessionid", session_id)

                # build our request data
                body = {
                    "csrfmiddlewaretoken": csrf_middleware_token,
                    "termination_b_location": aci_device.location.id,
                    "termination_b_device": aci_device.id,
                    "termination_b_id": aci_leaf_interface.id,
                    "status": connected_status.id
                }
                headers = {
                    "Content-Type": "application/x-www-form-urlencoded;",
                }

                # send the request to Nautobot to create the new connection
                post_res = requests.post(nautobot.base_url.replace("/api", "") + "/dcim/interfaces/" + xstr(interface_id) + "/connect/interface/",
                                         data=body, cookies=nautobot.http_session.cookies, headers=headers, timeout=5)
                # clear cookies now that they've been used
                nautobot.http_session.cookies.clear()
                module_interfaces_results.append((post_res, port.get("mac")))

            else:
                # TODO: support adding rack-mounted hardware that connects via VPC
                # this seemed to only exist for links between servers at HQ connected to border leafs
                print(
                    "WARN: ignoring a rack-mount device interface", interface_id, "because it connects to ACI via a VPC", aci_port_data)
        elif not port.get("mac"):
            # print(
            #     "DEBUG: found no mac associated with this port")
            pass
        else:
            print(
                "DEBUG: Ignoring a OneView MAC addr to one that does not exist in Cisco ACI", port.get("mac"))
    return module_interfaces_results


def create_ilo_interface_from_vpc(nautobot: Api, pc_collector: PortChannelCollector, vpc_name: str, node_ids: str, server: ServerHardware, nautobot_server_id: str, aci_node_names: dict, connected_status: str) -> requests.Response:
    for node in node_ids.split("-"):
        vpc_info = pc_collector.fetch_aci_node_lacp(node, False)
        print("vpc_info?", vpc_info)


def create_ilo_interfaces(nautobot: Api, ip_endpoint_collector: IpEndpointCollector, pc_collector: PortChannelCollector, server: ServerHardware, nautobot_server_id: str, aci_node_names: dict, connected_status: str) -> requests.Response:
    """
    Create iLO ethernet interface links between
    HPE OneView racked hardware and Cisco switches
    """
    if "mpHostInfo" in server:
        mgmt_proc_info = server.get("mpHostInfo")
        if mgmt_proc_info:
            if "mpIpAddresses" in mgmt_proc_info:
                for addr in mgmt_proc_info.get("mpIpAddresses"):
                    ipv4_addr_search = re.search(
                        "^((25[0-5]|(2[0-4]|1[0-9]|[1-9]|)[0-9])(.(?!$)|$)){4}$", addr.get("address"))
                    if ipv4_addr_search:
                        # fetch endpoint data from ACI
                        ipv4_addr = ipv4_addr_search.group(0)
                        (ethernet_port_name, aci_node_id,
                         aci_fex_id, aci_vpc_name, aci_mac) = ip_endpoint_collector.fetch_aci_endpoint_by_ip(ipv4_addr)
                        if not ethernet_port_name or not aci_node_id:
                            print("WARNING: did not find an IP endpoint while creating iLO connection for OneView server", server.get(
                                "name"), ". Does it use a VPC?", aci_vpc_name, "on nodes", aci_node_id, "with mac", aci_mac, "and ip", ipv4_addr)
                            create_ilo_interface_from_vpc(nautobot, pc_collector, aci_vpc_name, aci_node_id, server, nautobot_server_id, aci_node_names, connected_status)
                            continue
                        
                        server_interface_search = nautobot.dcim.interfaces.filter(
                            device=nautobot_server_id, module__isnull=True, name__ic='ilo')
                        if not server_interface_search:
                            print(
                                "WARN: could not locate a server when creating connections", nautobot_server_id)
                            continue
                        if server_interface_search[0].connected_endpoint:
                            print(
                                "DEBUG: a server iLO interface is already populated for device", nautobot_server_id)
                            continue
                        server_interface_id = server_interface_search[0].id

                        aci_node_name: str = aci_node_names[aci_node_id]
                        aci_device = nautobot.dcim.devices.filter(
                            name__ic=aci_node_name)
                        # if not found, give another search to accomodate human name entries
                        if not aci_device:
                            if "mgmt" in aci_node_name:
                                node_name = aci_node_name.replace("leaf", "")
                                aci_device = nautobot.dcim.devices.filter(
                                    name__ie=node_name)
                        if not aci_device:
                            print("ERROR: Found no matching ACI leaf device in Nautobot named: ",
                                  aci_node_name, " when creating iLO network interface connections.")
                            continue
                        else:
                            aci_device = aci_device[0]

                        # find FEX interface if a FEX port is reported
                        if aci_fex_id:
                            # print("DEBUG: searching for fex interface", ethernet_port_name,
                            #       "from node id", aci_node_id, "and fex id", aci_fex_id)
                            aci_fex_device_search = nautobot.dcim.devices.filter(
                                q="fex-"+aci_fex_id)
                            if aci_fex_device_search:
                                aci_device = aci_fex_device_search[0]
                                # print("DEBUG: found aci fex device!", aci_fex_device_search)
                            else:
                                print("WARN: found no ACI FEX device",
                                      aci_fex_id, "in Nautobot")

                            aci_leaf_interface_search = nautobot.dcim.interfaces.filter(
                                device=aci_device.id, name__iew=ethernet_port_name)
                        # if no FEX, find the device interface
                        else:
                            aci_leaf_interface_search = nautobot.dcim.interfaces.filter(
                                device=aci_device.id, name__ic=ethernet_port_name)

                        if not aci_leaf_interface_search:
                            print(
                                "ERROR: found no matching interface while searching for iLO's connected endpoint pair")
                            continue
                        else:
                            aci_leaf_interface = aci_leaf_interface_search[0]

                        if aci_leaf_interface.connected_endpoint:
                            # print("DEBUG: found a populated interface", aci_leaf_interface.id, "so we are skipping the re-population of its connection data")
                            continue

                        # build our request metadata
                        nautobot.http_session.cookies.clear()
                        csrf_middleware_token: str
                        (csrf_token, csrf_middleware_token) = fetch_nautobot_form_content(
                            nautobot, nautobot.base_url.replace("/api", "") + "/dcim/interfaces/", "csrfmiddlewaretoken")
                        nautobot.http_session.cookies.set(
                            "csrftoken", csrf_token)
                        session_id = fetch_nautobot_sessionid(
                            nautobot, csrf_middleware_token)
                        nautobot.http_session.cookies.set(
                            "sessionid", session_id)

                        # build our request data
                        body = {
                            "csrfmiddlewaretoken": csrf_middleware_token,
                            "termination_b_location": aci_device.location.id,
                            "termination_b_device": aci_device.id,
                            "termination_b_id": aci_leaf_interface.id,
                            "status": connected_status.id
                        }
                        headers = {
                            "Content-Type": "application/x-www-form-urlencoded;",
                        }

                        # send the request to Nautobot to create the new connection
                        post_res = requests.post(nautobot.base_url.replace("/api", "") + "/dcim/interfaces/" + xstr(server_interface_id) + "/connect/interface/",
                                                 data=body, cookies=nautobot.http_session.cookies, headers=headers, timeout=5)
                        # clear cookies now that they've been used
                        nautobot.http_session.cookies.clear()
                        return post_res


def create_device_module_interfaces(nautobot: Api, aci_session: Session, oneview_hardware: list[ServerHardware], filtered_aci_infos: dict, aci_node_names: dict):
    """
    # oneview_hardware includes only the devices that had non_iLO MAC addresses appear in ACI
    # their iLO data is brought with them, but this means that a server rack with nothing more than an iLO interface will not appear here
    :oneview_hardware: a list of ServerHardware that has MACS which appeared in ACI
    :filtered_aci_infos: a list of aci data (secondary lookup table)
    """
    results: list[list[tuple[requests.Response, str]]] = []

    connected_status = nautobot.extras.statuses.filter(name__ie="Connected")[0]
    ip_endpoint_collector: IpEndpointCollector = IpEndpointCollector(
        aci_session)
    pc_collector: PortChannelCollector = PortChannelCollector(aci_session)

    for server in oneview_hardware:

        # some shared lookups
        if "portMap" in server:
            server_search: list[Record] = nautobot.dcim.devices.filter(
                name__ie=re.sub("(ilo)(?=$|[.\n]{1})", "", server.get("name")))
            server_id: str = server_search[0].id

        # handle iLO interfaces
        create_ilo_interfaces(nautobot, ip_endpoint_collector, pc_collector,
                              server, server_id, aci_node_names, connected_status)

        # handle non-iLO interfaces
        if "portMap" in server:
            if server.get("portMap"):
                for module_slot in server.get("portMap"):
                    for nic in server.get("portMap")[module_slot]:
                        # find NIC module
                        location: str = nic.get("location").lower()
                        match location:
                            case "flr":
                                position = "FlexLOM"
                            case "pci":
                                position = "PCIe" + str(nic.get("slotNumber"))
                            case "lom":
                                position = None
                            case "ocp":
                                position = "OCP3"

                        results.append(create_interfaces(
                            nautobot, server_id, nic, position, connected_status, filtered_aci_infos, aci_node_names))

    return results


def list_node_ids(aci_infos: dict) -> tuple[set[str], None]:
    """
    given a dict of objects like the one below
    "00: 50: 56:A6:E2:E6": {
        "00: 50: 56:A6:E2:E6": {
        "ip": "167.161.183.213",
        "secondary_ip": [],
        "if_dn": [],
        "encap": "vlan-182",
        "if_name": "eth 1/210/1/22"
    }
    parse if_name to find each unique node id.
    We return a tuple so we can share functions from aci_helpers.py
    """
    node_id_list: set[str] = set([])
    # create ACI node name to id map
    for mac in aci_infos:
        encoded_node = aci_infos[mac].get("if_name")
        node_id = re.search("(?<=eth [0-9]{1}/)([0-9]{3})(?=/)", encoded_node)
        if node_id:
            # print("found node id", node_id.group(0))
            node_id_list.add((node_id.group(0), None))
    return node_id_list


def create_server_role(nautobot: Api):

    nautobot.http_session.cookies.clear()
    csrf_middleware_token: str
    (csrf_token, csrf_middleware_token) = fetch_nautobot_form_content(nautobot,
                                                                      nautobot.base_url.replace("/api", "") + "/dcim/locations/", "csrfmiddlewaretoken")
    nautobot.http_session.cookies.set("csrftoken", csrf_token)
    session_id = fetch_nautobot_sessionid(nautobot, csrf_middleware_token)
    nautobot.http_session.cookies.set("sessionid", session_id)

    body = MultipartEncoder(
        fields={
            "csrfmiddlewaretoken": csrf_middleware_token,
            "name": "Server",
            "description": "Server role created with py_populate_dcim for HPE OneView racked servers",
            "content_types": "3",  # dcim | device,
            "color": "ffffff"
        })

    hederz = {
        "Content-Type": body.content_type,
    }
    post_res: requests.Response = requests.post(nautobot.base_url.replace("/api", "") + "/extras/roles/add/",
                                                data=body, cookies=nautobot.http_session.cookies, headers=hederz, timeout=5)
    # clear cookies now that they've been used
    nautobot.http_session.cookies.clear()

    return post_res
