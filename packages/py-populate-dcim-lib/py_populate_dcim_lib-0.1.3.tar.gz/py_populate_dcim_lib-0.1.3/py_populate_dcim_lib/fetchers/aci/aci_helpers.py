from argparse import Namespace
import sys
import re
import etherflow_acitoolkit as aci
from etherflow_acitoolkit.acisession import Session
from etherflow_acitoolkit import (
    Endpoint,
)
from etherflow_acitoolkit.aciphysobject import Node
import time

from ...debug.stand_in_objects import (
    filtered_aci_example,
    aci_macs_example,
    cisco_node_names_example,
)
from ...fetchers.aci.aci_port_channel import PortChannelCollector
from ...fetchers.helpers import keys_exists
import requests


def auth_cisco_aci(args: Namespace) -> Session:
    # Take login credentials from the command line if provided
    # Otherwise, take them from your environment variables file ~/.profile
    description = (
        "Simple application that logs on to the APIC"
        " to fetch connected MAC and IP addrs."
    )
    creds = aci.Credentials("apic", description)
    creds_args, creds_unknownargs = creds._parser.parse_known_args()

    resp = None
    if not args.debug:
        # Login to APIC
        # see if APIC endpoint is reachable before trying to log in (without this, the server keeps trying to refresh the connection)
        try:
            response = requests.get(creds_args.url, verify=False, timeout=5)
            if response.ok:   # alternatively you can use response.status_code == 200
                print("DEBUG: Success - APIC API is accessible.")
            else:
                print(
                    f"DEBUG: Failure - APIC API is accessible but sth is not right. Response code : {response.status_code}")
        except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
            print(
                f"DEBUG: Failure - Unable to establish APIC connection: {e}.")
            return "502"
        except Exception as e:
            print(
                f"DEBUG: Failure - Unknown error occurred when connecting to APIC: {e}.")
            return "503"

        print("INFO: Connecting to APIC...")
        session = aci.Session(
            creds_args.url, creds_args.login, creds_args.password)
        resp = session.login()
        if not resp.ok:
            print("ERROR: Could not login to APIC")
            # sys.exit(1)
            return "500"
        else:
            print("INFO: Connected to APIC!")
    else:
        print("DEBUG: debug mode enabled - not connecting to APIC")
        session = None
    return session


def map_aci_node_names(session: Session | None, node_ids: list[tuple] | set[tuple] | None, args: bool = False) -> dict:
    '''
    use arg --fetchall to run a new query for ACI node names.
    This process is slow, so I've hard-coded the state which is returned when fetchall is false (default)
    '''
    pod_list = []
    cisco_node_names = {}

    if args.fetchall:
        # identify possible pods to search for Nodes from
        pods = aci.Pod.get(session)
        for pod in pods:
            pod_list.append(pod.pod)

        for (node_id, vpc_id) in node_ids:
            for pod in pod_list:
                print("DEBUG: searching in pod:", pod)
                items = aci.Node.get(
                    session, parent=pod, node_id=node_id
                )
                if items:
                    print("DEBUG: found a matching ACI node: ", items)
                    break
                else:
                    print("DEBUG: looping to find match in other pod")
                    continue
            for item in items:
                cisco_node_names[node_id] = item.name
    else:
        cisco_node_names = {'414': 'MTleaf16OB', '413': 'MTleaf16OA', '412': 'MTleaf16KB', '411': 'MTleaf16KA', '212': 'NDCleaf08OB', '211': 'NDCleaf08OA', '218': 'NDCleaf11KB',
                            '217': 'NDCleaf11KA', '219': 'NDCleaf11GA', '220': 'NDCleaf11GB', '209': 'NDCleaf03GA', '210': 'NDCleaf03GB', '408': 'MTleaf08LB', '407': 'MTleaf08LA'} | {'217': 'NDCleaf11KA',
                            '216': 'NDCleaf11OB', '218': 'NDCleaf11KB', '409': 'MTleaf11PA', '411': 'MTleaf16KA', '203': 'NDCborderwestA', '205': 'NDCmgmtleafA', '401': 'MTborder03MA',
                            '506': 'MTmgmtleaf16K', '405': 'MTleaf03QA', '402': 'MTborder03MB', '207': 'NDCleaf03KA', '502': 'MTmgmtleaf08P', '221': 'NDCleaf16FA', '501': 'MTmgmtleaf03M',
                            '406': 'MTleaf03QB', '413': 'MTleaf16OA', '211': 'NDCleaf08OA', '414': 'MTleaf16OB', '214': 'NDCleaf08KB', '410': 'MTleaf11PB', '213': 'NDCleaf08KA',
                            '404': 'MTborder08PB', '201': 'NDCbordereastA', '206': 'NDCmgmtleafB', '503': 'MTmgmtleaf03Q', '208': 'NDCleaf03KB', '504': 'MTmgmtleaf08L', '209': 'NDCleaf03GA',
                            '210': 'NDCleaf03GB', '224': 'NDCleaf11OD', '415': 'MTleaf18DA', '212': 'NDCleaf08OB', '412': 'MTleaf16KB', '505': 'MTmgmtleaf11P', '222': 'NDCleaf16FB',
                            '507': 'MTmgmtleaf16O', '403': 'MTborder08PA', '219': 'NDCleaf11GA', '204': 'NDCborderwestB', '508': 'MTmgmtleaf18D', '202': 'NDCbordereastB', '416': 'MTleaf18DB', '215': 'NDCleaf11OA', '223': 'NDCleaf11OC'}

    return cisco_node_names

##############################
# For OneView Synergy Frames #
##############################


def populate_pair_aci_data(aci_node_name_map: dict, pairs: dict) -> dict:
    for link in pairs:
        node_id = re.search("(?<=node-)([0-9]*)(?=/)", link).group(0)
        # pairs[link]['aciNodeId'] = node_id
        pairs[link]['aci']['nodeName'] = aci_node_name_map[node_id]
        eth_port = re.search("(?<=if-\\[)(.*)(?=\\])", link).group(0)
        pairs[link]['aci']['portLoc'] = eth_port

    return pairs


###########################################
# For OneView Server Rack HW (no Synergy) #
###########################################

def poll_aci_endpoints(session: Session, args: Namespace) -> tuple[frozenset, dict]:
    """
    Fetch MAC addrs and corresponding IP addrs from CISCO ACI API
    :return: tuple[frozenset, dict]
    """

    macs = None
    aci_infos = None
    if not args.debug:
        # Download all of the IPEndpoint
        # and store the data as a set and dictionary
        macs: list[str] = []
        aci_infos: dict = {}

        eps: list[Endpoint] = aci.Endpoint.get(session)
        for ep in eps:
            ep_data = {}
            ep_data["ip"] = ep.ip
            # ep_data["encap"] = ep.encap
            ep_data["secondary_ip"] = ep.secondary_ip
            ep_data["if_dn"] = ep.if_dn
            ep_data["encap"] = ep.encap
            ep_data["if_name"] = ep.if_name
            aci_infos[ep.mac] = ep_data
            # list of MAC addresses for comparison
            macs.append(ep.mac)
        # Construct a set from the list of MAC addresses
        macs = frozenset(macs)
    else:
        print("Debug enabled - not polling Cisco ACI for Endpoints")
        aci_infos = filtered_aci_example
        macs = aci_macs_example

    return (macs, aci_infos)


def filter_aci_endpoints(aci_macs: frozenset, aci_infos: dict, filter_names: list[str]) -> tuple[frozenset, dict]:
    '''
    given a set of MAC addrs from ACI 
    and a dictionary of corresponding ACI endpoints
    filter out any endpoints with interface names in `filter_names`
    then return a tuple containing the filtered-out set of MACs and a filtered-out dictionary of relevant endpoints
    '''
    filtered_aci_macs = set(aci_macs.copy())
    filtered_aci_infos = aci_infos.copy()
    for index, mac_addr in enumerate(aci_macs):
        if_dn: str
        for if_dn in aci_infos[mac_addr].get("if_dn"):
            for unwanted_str in filter_names:
                if unwanted_str.lower() in if_dn.lower():
                    # print("DEBUG: omitting an unwanted ACI endpoint due to if_dn name", unwanted_str, if_dn)
                    if mac_addr in filtered_aci_macs:
                        filtered_aci_macs.remove(mac_addr)
                        del filtered_aci_infos[mac_addr]
                    continue
    return (frozenset(filtered_aci_macs), filtered_aci_infos)

#################################
# the functions below go unused #
#################################


def poll_aci_lacp(session: Session) -> tuple[dict, set]:
    interface_collector = PortChannelCollector(session)
    aci_lacp_infos = interface_collector.fetch_aci_lacp()
    singlenode_lacp_builder = {}
    aci_lacp_withneighbors: dict = {}
    aci_adjacent_macs: set = set([])
    # collect ACI's adjacent Mac addresses and LACP port IDs
    lacp_node_id: str
    for lacp_node_id in aci_lacp_infos:
        if lacp_node_id and aci_lacp_infos[lacp_node_id]:
            lacp_if: dict
            aci_lacp_withneighbors[lacp_node_id] = {}
            for lacp_if in aci_lacp_infos[lacp_node_id]:
                neighbor_entry: dict = {}
                if keys_exists(lacp_if, "lacpIf", "attributes"):
                    dn = re.findall(r"(?<=pod-).*?(?=/)",
                                    lacp_if['lacpIf']['attributes']['dn'])
                    aci_lacp_withneighbors[lacp_node_id]['pod'] = dn[0]
                if keys_exists(lacp_if, "lacpIf", "children"):
                    for child in lacp_if['lacpIf']['children']:
                        if keys_exists(child, "lacpAdjEp"):
                            neighbor_entry["adjPort"] = child["lacpAdjEp"]["attributes"]["port"]
                            singlenode_lacp_builder[child["lacpAdjEp"]
                                                    ["attributes"]["sysId"]] = neighbor_entry
                            aci_adjacent_macs.add(
                                child["lacpAdjEp"]["attributes"]["sysId"])
            aci_lacp_withneighbors[lacp_node_id]['adjLacp'] = singlenode_lacp_builder

    return (aci_lacp_withneighbors, aci_adjacent_macs)


def poll_aci_nodes(session: Session, data: dict) -> dict:
    start = time.time()
    for node_id in data:
        items: Node = Node.get(session, node_id=node_id,
                               parent=data[node_id]['pod'])
        for item in items:
            data[node_id]["name"] = item.name
    end = time.time()
    timed = end-start
    print("it took", timed, "seconds to poll Nodes")
    return data


def map_cisco_node_names(
    session: Session, filtered_aci_infos: dict, debug: bool
) -> dict:
    '''
    deprecated and succeeded by map_aci_node_names()
    '''
    cisco_node_names = {}
    pod_list = []

    if not debug:
        # identify possible pods to search for Nodes from
        pods = aci.Pod.get(session)
        for pod in pods:
            pod_list.append(pod.pod)

        start = time.time()
        for node in filtered_aci_infos:
            items = None
            # print("~~~")
            # print("searching for node ID of", filtered_aci_infos[node]['if_name'])
            node_id = re.search(
                "(?<=eth [0-9]/)([0-9]*)(?=/{1})", filtered_aci_infos[node]["if_name"]
            )
            if node_id != None:
                for pod in pod_list:
                    # print("searching in pod:", pod)
                    items = aci.Node.get(
                        session, parent=pod, node_id=str(node_id.group(0))
                    )
                    if items != []:
                        # print("found a matching ACI node: ", items)
                        break
                    else:
                        # print("looping to find match in other pod")
                        continue
            else:
                print("failed to regex search for node_id")

            for item in items:
                cisco_node_names[node] = item.name

        end = time.time()
        spent = end - start
        print("it took ", spent, "to fetch filtered set of Nodes")
    else:
        print("Debug enabled - not fetching CISCO Pods or Nodes")
        cisco_node_names = cisco_node_names_example
    return cisco_node_names
