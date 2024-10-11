"""OneView interface for rack-mounted servers managed via VMWare VSphere composer"""
from argparse import Namespace
from hpeOneView.resources.servers.server_hardware import ServerHardware
from hpeOneView.oneview_client import OneViewClient


# create a set with all unique mac addrs
# create a dict of modules (location and slot number) that need to be populated into each device
# create a sub-dictionary of all unique mac addrs (with populated port number) that need to be added to each module


# to populate these macs on the HPE server side
# update each device to contain module bays
# populate the module bay with the module that we found in the object above

def fetch_oneview_server_hardware(args: Namespace) -> list[ServerHardware]:
    '''
    Get all server_profiles from OneView
    return a list of ServerHardware
    '''

    oneview_client = OneViewClient.from_environment_variables()
    print("DEBUG: Fetching all server hardware from HPE OneView")
    hardware_all: list[ServerHardware] = oneview_client.server_hardware.get_all()
    return hardware_all


def find_oneview_server_hardware_unique_attrs(oneview_hardware: list[ServerHardware]) -> tuple[set, set]:
    server_device_types = set([])
    # enumerates each unique NIC hardware type to be imported as a Nautobot module
    nic_module_types = set([])

    for server in oneview_hardware:
        model = server.get("model")
        server_device_types.add(model)
        if "portMap" in server:
            # print("server", server)
            if server.get("portMap"):
                for slots in server.get("portMap"):
                    # print("slots", json.dumps(server.get("portMap")[slots]))
                    for nic in server.get("portMap")[slots]:
                        # print(nic)
                        nic_module_types.add(nic.get("deviceName"))

    return (server_device_types, nic_module_types)


def find_oneview_server_hardware_unique_macs(oneview_hardware: list[ServerHardware]) -> set:
    oneview_macs = set([])

    for server in oneview_hardware:
        if "portMap" in server:
            # print("server", server)
            if server.get("portMap"):
                for slots in server.get("portMap"):
                    # print("slots", json.dumps(server.get("portMap")[slots]))
                    for nic in server.get("portMap")[slots]:
                        # print(nic)
                        for port in nic.get("physicalPorts"):
                            oneview_macs.add(port.get("mac"))

    return oneview_macs


def build_oneview_infos_from_macs(oneview_hardware: list[ServerHardware], macs: frozenset | set | list[str]):
    all_hardware_names: set[str] = set([])
    filtered_hardware: list[ServerHardware] = []
    filtered_hardware_names: set[str] = set([])
    ignored_hardware_ports: set[tuple[str, str]] = set([])
    ignored_hardware_names: set[str] = set([])
    for server in oneview_hardware:
        if server.get("name") in all_hardware_names:
            print("WARN FOUND A DUPLICATE SERVER NAME!", server.get("name"))
        if len(server.get("name")) < 2:
            print("WARN: FOUND SHORT SERVER NAME", server.get("name"))
        all_hardware_names.add(server.get("name"))
        # select which oneview records to return
        # only return those devices that have relevant MAC addresses
        if "portMap" in server:
            if server.get("portMap"):
                for slots in server.get("portMap"):
                    for nic in server.get("portMap")[slots]:
                        for port in nic.get("physicalPorts"):
                            if port.get("mac") in macs:
                                # filtered_hardware.append(server)
                                filtered_hardware_names.add(server.get("name"))
                            else:
                                ignored_hardware_ports.add(
                                    (server.get("name"), port.get("mac")))
                                ignored_hardware_names.add(server.get("name"))
    ignored_hardware_names = ignored_hardware_names - filtered_hardware_names
    servers_without_ports = all_hardware_names - \
        ignored_hardware_names - filtered_hardware_names
    # print("WARN: the following OneView (server, MAC) did not find a match in ACI:")
    # pprint(ignored_hardware_ports)

    # print("INFO: total number of OneView servers", len(oneview_hardware))
    # print("DEBUG: no ports on", len(servers_without_ports), "OneView servers:", servers_without_ports)

    # print("DEBUG: filtered out OneView servers with no matching MAC addrs", len(ignored_hardware_names))
    # pprint(ignored_hardware_names)

    # print("DEBUG: matched OneView servers by MAC", len(filtered_hardware_names))
    # pprint(filtered_hardware_names)

    for server in oneview_hardware:
        if server.get("name") in filtered_hardware_names:
            filtered_hardware.append(server)

    # print("DEBUG: Returning", len(filtered_hardware), "servers with connected MAC addresses")
    # pprint(filtered_hardware)
    return filtered_hardware
