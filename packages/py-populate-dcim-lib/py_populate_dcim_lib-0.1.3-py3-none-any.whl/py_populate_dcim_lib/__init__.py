"""
Application that logs on to the APIC and fetches all of the endpoint IPs and MAC addresses.
It then compares CISCO ACI endpoints to OneView's Synergy composer interfaces to find pairs.
"""
import os
import sys
import json
from argparse import Namespace, BooleanOptionalAction, ArgumentParser
from pathlib import Path
from dotenv import load_dotenv
from py_populate_dcim_lib.fetchers.nautobot.device_and_module_types import import_new_nautobot_types
from pynautobot.core.api import Api
from pynautobot.models.dcim import Devices, Interfaces
from hpeOneView.resources.servers.server_hardware import ServerHardware
from etherflow_acitoolkit.acisession import Session
from .fetchers.nautobot.nautobot_vmware_vsphere import create_device_module_interfaces, create_oneview_server_devices, create_oneview_server_modules, list_node_ids
from .fetchers.nautobot.nautobot_virtual_connects import create_missing_vc_devices, create_missing_vc_interfaces, fetch_nautobot_device_interfaces, fetch_nautobot_vc_dict, find_frames_missing_vc_devices
from .fetchers.oneview.vmware_vsphere import build_oneview_infos_from_macs, fetch_oneview_server_hardware, find_oneview_server_hardware_unique_attrs, find_oneview_server_hardware_unique_macs
from .fetchers.aci.aci_endpoint_vpcs import VpcCollector
from .fetchers.aci.aci_port_channel import PortChannelCollector
from .fetchers.aci.aci_helpers import auth_cisco_aci, filter_aci_endpoints, map_aci_node_names, poll_aci_endpoints, populate_pair_aci_data
from .fetchers.helpers import merge_args
from .fetchers.nautobot.nautobot import fetch_check_nautobot_devices_vs_aci, fetch_check_nautobot_frames_vs_oneview
from .fetchers.nautobot.nautobot_helpers import auth_nautobot_api
from .fetchers.oneview.synergy_virtual_connects import format_one_view_data, populate_pair_oneview_synergy_data


def aggregate_oneview_synergy_aci_vpc_pairs(aci_portchannel_collector: PortChannelCollector, aci_node_ids: list[tuple], oneview_macs: set, debug: bool = False) -> dict[dict]:
    '''
    returns a dictionary containing key-value mappings between
    ACI interfaces (as the key) and oneview lacp ports(as values)
    '''
    vpc_bridges = {}
    all_lacp_policies = {}
    for (node, vpc) in aci_node_ids:
        lacp_policy = aci_portchannel_collector.fetch_aci_node_lacp(
            node, debug)
        # print("lacp", json.dumps(lacp_policy, indent=4))
        for node in lacp_policy:
            all_lacp_policies[node] = lacp_policy
            for lacp_if in lacp_policy[node]:
                for child in lacp_if['lacpIf']['children']:
                    if child.get('lacpAdjEp'):
                        if any(child['lacpAdjEp']['attributes']['sysId'] in x for x in oneview_macs):
                            oneview_port_channel = {}
                            oneview_port_channel['oneView'] = {}
                            oneview_port_channel['oneView']['sysId'] = child['lacpAdjEp']['attributes']['sysId']
                            oneview_port_channel['oneView']['port'] = child['lacpAdjEp']['attributes']['port']
                            oneview_port_channel['aci'] = {}
                            oneview_port_channel['aci']['vpcName'] = vpc
                            vpc_bridges[lacp_if['lacpIf']['attributes']
                                        ['dn']] = oneview_port_channel
    # print(json.dumps(all_lacp_policies, indent=4))
    return vpc_bridges


def match_oneview_and_aci_lacp(args: Namespace, aci_session: Session, aci_node_names: dict):
    # parse through CSV of LACP data from OneView (pulled manually)
    (oneview_lacp, oneview_macs) = format_one_view_data(args.debug)

    # create ACI helpers
    aci_vpc_collector: VpcCollector = VpcCollector(aci_session)
    aci_pc_collector = PortChannelCollector(aci_session)

    # parse through ACI and fetch the VPCs that have relevant names
    relevant_vpc_names = ['synergy', 'synframe']
    (endpoint_vpcs, vpc_set) = aci_vpc_collector.get_endpoint_vpcs(
        relevant_vpc_names, args.debug)
    # vpc_collector._display_endpoint_vpcs(endpoint_vpcs)
    # print("vpc_set", vpc_set)

    # given the relevant vpcs, fetch their details
    vpc_children = aci_vpc_collector.get_vpc_children(vpc_set, args.debug)
    # print("vpc_children", json.dumps(vpc_children, indent=4))

    # create list of node_ids that came from the relevant VPCs
    vpc_node_ids: list = []
    for vpc in vpc_children:
        for node in vpc_children[vpc]:
            vpc_node_ids.append((node, vpc))

    # tie OneView ports to ACI ports
    # print("aggregating oneview_synergy_aci_vpc_pairs")
    aci_oneview_pairs = aggregate_oneview_synergy_aci_vpc_pairs(
        aci_pc_collector, vpc_node_ids, oneview_macs, args.debug)

    # populate OneView locations from LACP data
    aci_oneview_pairs = populate_pair_oneview_synergy_data(
        oneview_lacp, aci_oneview_pairs)

    aci_oneview_pairs = populate_pair_aci_data(
        aci_node_names, aci_oneview_pairs)

    return aci_oneview_pairs


def populate_nautobot_with_oneview_aci_pairs(args: Namespace):

    # shared resources
    nautobot: Api = auth_nautobot_api()
    aci_session: Session = auth_cisco_aci(args)

    # fetch *all* ACI endpoints
    (aci_macs, aci_infos) = poll_aci_endpoints(aci_session, args)
    aci_node_ids = list_node_ids(aci_infos)

    # TODO: expose this last arg to UI options
    # map *all* ACI endpoint IDs to their names
    aci_node_names = map_aci_node_names(
        aci_session, aci_node_ids, args)

    # begin user-selectable modes

    # Import Nautobot Types
    if args.import_nautobot_types:
        print("INFO: Creating and updating Nautobot Device Types and Module Types")
        import_new_nautobot_types(nautobot)
    else:
        print("DEBUG: NOT creating and updating Nautobot Device Types and Module Types because arg import_nautobot_types was not True")

    # Synergy Frames
    if args.refresh_synergy_frames:
        oneview_aci_pairs = match_oneview_and_aci_lacp(
            args, aci_session, aci_node_names)
        # print("oneview_aci_pairs", json.dumps(oneview_aci_pairs, indent=4))

        aci_nodename_set: set[str] = set([])
        oneview_frame_set: set[str] = set([])
        oneview_frame_models: set[tuple[str]] = set([])
        for pair in oneview_aci_pairs:
            aci_nodename_set.add(
                oneview_aci_pairs[pair].get("aci").get("nodeName"))
            oneview_frame_set.add(
                oneview_aci_pairs[pair].get("oneView").get("frame"))
            oneview_frame_models.add((oneview_aci_pairs[pair].get("oneView").get(
                "frame"), oneview_aci_pairs[pair].get("oneView").get("model")))
        oneview_frame_models: dict = dict(oneview_frame_models)

        # fetch ACI devices and interfaces from nautobot
        nautobot_aci_leaf_devices: list[Devices] = fetch_check_nautobot_devices_vs_aci(
            nautobot, ["NDCleaf", "MTleaf"], aci_nodename_set)
        nautobot_aci_device_interfaces: dict[Interfaces] = fetch_nautobot_device_interfaces(
            nautobot, nautobot_aci_leaf_devices)

        # fetch OneView FRAME devices and interfaces from nautobot
        nautobot_oneview_frame_devices: list[Devices] = fetch_check_nautobot_frames_vs_oneview(
            nautobot, oneview_frame_set, oneview_frame_set)
        print("nautobot_oneview_frame_devices", nautobot_oneview_frame_devices)
        # SYNFRAME devices do not contain their own interfaces, so they are ignored
        # nautobot_oneview_frame_interfaces: dict[Interfaces] = fetch_nautobot_device_interfaces(nautobot, nautobot_oneview_frame_devices) # this is mostly empty. instead, child devices contain the interfaces for now (until modules are supported by pynautobot SDK)

        # fetch the existing OneView Virtual Connect devices from nautobot
        # includes their device bays and parents
        nautobot_oneview_vc_devices: dict = fetch_nautobot_vc_dict(
            nautobot, "Virtual Connect", nautobot_oneview_frame_devices)

        # for every SYNFRAME that does not have an associated Virtual Connect
        # tuple[list[Devices]]
        nautobot_oneview_frames_without_vc = find_frames_missing_vc_devices(
            nautobot_oneview_vc_devices, nautobot_oneview_frame_devices)

        # create the Virtual Connect devices
        # this step also associates new and existing Virtual Connect devices to their Synergy Frame
        # (list[Devices])
        (new_vc_devices_result, new_vc_children_result) = create_missing_vc_devices(
            nautobot, nautobot_oneview_frames_without_vc, oneview_frame_models, oneview_aci_pairs)

        # fetch nautobot Viritual Connect interfaces (ordered by rear bay number)
        # tuple[dict[list[Interfaces]]]
        new_vc_device_interfaces_result = create_missing_vc_interfaces(
            nautobot, oneview_aci_pairs)
    else:
        print("DEBUG: Not updating Synergy Frame network locations or connections since arg update_synergy_frames was not set")

    # create common Racked Server contents
    if args.create_oneview_server_devices or args.create_oneview_server_modules or args.create_oneview_server_interfaces:
        print("INFO: Updating HPE server network locations to Nautobot!")

        # filter out ACI endpoints to not include Synergy Frames
        (filtered_aci_macs, filtered_aci_infos) = filter_aci_endpoints(
            aci_macs, aci_infos, ["synframe", "synergy"])

        all_oneview_hardware: list[ServerHardware] = fetch_oneview_server_hardware(
            args)
        all_oneview_macs = find_oneview_server_hardware_unique_macs(
            all_oneview_hardware)

        matched_macs: frozenset = filtered_aci_macs.intersection(
            all_oneview_macs)

        oneview_hardware: list[ServerHardware] = build_oneview_infos_from_macs(
            all_oneview_hardware, matched_macs)
        # (oneview_server_types, oneview_nic_module_types) = find_oneview_server_hardware_unique_attrs(
        #     oneview_hardware)

        if args.create_oneview_server_devices:
            oneview_new_servers = create_oneview_server_devices(
                nautobot, oneview_hardware)

        if args.create_oneview_server_modules:
            oneview_new_modules = create_oneview_server_modules(
                nautobot, oneview_hardware)

        if args.create_oneview_server_interfaces:
            new_device_interfaces_result = create_device_module_interfaces(
                nautobot, aci_session, oneview_hardware, filtered_aci_infos, aci_node_names)

    else:
        print("DEBUG: Not updating HPE Server device network locations or connections since arg update_hpe_servers was not True")

    if not args.debug:
        # close ACI session
        aci_session.close()
    return


def create_args() -> Namespace:
    parser = ArgumentParser(
        prog="py-populate-dcim",
        description="Poll Cisco ACI and OneView to match MAC addresses and physical port names.",
        epilog="See docs at https://git.autonaut.dev/autonaut/py-populate-dcim",
    )
    parser.add_argument(
        "--debug",
        help="set --debug to enable debugging mode which does not make API calls to ACI or OneView. This uses previously-fetched hard-coded data.",
        action=BooleanOptionalAction,
    )
    parser.add_argument(
        "--fetchall",
        help="set --fetchall to fetch from the ACI API that doesn't normally change between runs.",
        action=BooleanOptionalAction,
    )
    parser.add_argument(
        "--refresh-synergy-frames",
        help="set --refresh-synergy-frames fetch for new Synergy Frames and to link them to Cisco ACI ports via Virtual Port Channel and LACP metadata",
        action=BooleanOptionalAction,
    )
    parser.add_argument(
        "--create_oneview_server_devices",
        help="set --create-oneview-server-devices to fetch for new HPE Servers from OneView and create them in Nautobot",
        action=BooleanOptionalAction,
    )
    parser.add_argument(
        "--create_oneview_server_modules",
        help="set --create-oneview-server-modules to populate Nautobot's HPE Servers with their networking modules based on OneView data",
        action=BooleanOptionalAction,
    )
    parser.add_argument(
        "--create_oneview_server_interfaces",
        help="set --create-oneview-server-interfaces to populate Nautobot's HPE Servers with their networking modules based on OneView data",
        action=BooleanOptionalAction,
    )
    parser.add_argument(
        "--import-nautobot-types",
        help="set --import-nautobot-types to write Device Types and Module Types stored in /nautobot-types/",
        action=BooleanOptionalAction,
    )
    (args, unknown_args) = parser.parse_known_args()
    return args


def api_main(api_args: Namespace | None):
    try:
        # check if required environment variables are defined
        env_vars: list = [
            "APIC_URL",
            "APIC_LOGIN",
            "APIC_PASSWORD",
            "ONEVIEWSDK_USERNAME",
            "ONEVIEWSDK_PASSWORD",
            "ONEVIEWSDK_IP",
            "NAUTOBOT_URL",
            "NAUTOBOT_USER",
            "NAUTOBOT_PASSWORD"
        ]
        for env_var in env_vars:
            if os.getenv(env_var):
                pass
            else:
                print(
                    "WARN: attempting to continue without a required environment variable for py_populate_dcim_lib: ", env_var)

        args: Namespace = create_args()
        # merge API request body and CLI argument flags
        if api_args:
            # second argument overrides first one. This means that an API call's POST object will overwrite cli flags
            args = merge_args(args, api_args)

        populate_nautobot_with_oneview_aci_pairs(args)
        print("INFO: Etherflow's py-populate-dcim app has successfully completed a pass")
        return "OK"
    except KeyboardInterrupt:
        pass
    return


# oneshot the program if the user runs main.py
if __name__ == "__main__":
    try:
        env_file_path: str = os.environ.get('CONFIG_PATH', '.env')
        # assure the user has provided a .env file for credentials
        if not Path(env_file_path).is_file():
            print(
                "ERROR: could not find your configuration file at path: ", env_file_path)
            sys.exit("ERROR: you must provide a .env file")
        else:
            load_dotenv()
        args: Namespace = create_args()
        populate_nautobot_with_oneview_aci_pairs(args)
    except KeyboardInterrupt:
        pass
