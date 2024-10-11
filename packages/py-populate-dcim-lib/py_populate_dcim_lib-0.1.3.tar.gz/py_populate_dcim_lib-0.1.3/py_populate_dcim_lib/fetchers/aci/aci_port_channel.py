#!/usr/bin/env python
"""
This application replicates the switch CLI command 'show port-channel summary'
It largely uses raw queries to the APIC API
"""
import json
from etherflow_acitoolkit import Credentials, Session, Endpoint, EPG
import etherflow_acitoolkit as aci
from etherflow_acitoolkit.aciphysobject import WorkingData, Node
from tabulate import tabulate
from ...debug.stand_in_objects import fetch_aci_lacp_lacp_infos


class PortChannelCollector(object):
    def __init__(self, session: Session):
        # Login to APIC
        self._apic = None
        self._apic = session
        self._interfaces = []
        self._port_channels = []

    def _get_query(self, query_url, error_msg) -> list:
        resp = self._apic.get(query_url)
        if not resp.ok:
            print(error_msg)
            print(resp.text)
            return []
        return resp.json()['imdata']

    def get_node_ids(self, node_id):
        """
        Get the list of node ids from the command line arguments.
        If none, get all of the node ids
        :param args: Command line arguments
        :return: List of strings containing node ids
        """
        if node_id is not None:
            names = [node_id]
        else:
            names = []
            query_url = ('/api/node/class/fabricNode.json?'
                         'query-target-filter=eq(fabricNode.role,"leaf")')
            error_message = 'Could not get switch list from APIC.'
            nodes = self._get_query(query_url, error_message)
            for node in nodes:
                names.append(str(node['fabricNode']['attributes']['id']))
        return names

    # def get_epgs(self, debug: bool = False):
    #     if not debug:
    #         data: dict = {}
    #         port_channels = set([])
    #         endpoint_groups: list[EPG] = aci.EPG.get(self._apic)
    #         for epg in endpoint_groups:
    #             epg_entry: dict = {}
    #             app_profile = epg.get_parent()
    #             tenant = app_profile.get_parent()
    #             print("ap and tn", app_profile, tenant)
    #             # print("epg", epg.get_json())
    #             # query_url = f"api/node/mo/uni/tn-NDC/ap-NDC-Net-ANP/epg-150_ACI_MGMT-EPG.json?query-target=children&target-subtree-class=fvCEp&query-target-filter=and(not(wcard(fvCEp.dn,"__ui_")),eq(fvCEp.lcC,"learned"))&rsp-subtree=children&rsp-subtree-class=fvRsCEpToPathEp,fvIp&subscription=yes&order-by=fvCEp.mac|asc&page=0&page-size=15&_dc=1727279026362"
    #         return (data, port_channels)
    #     else:
    #         print("WARN: get_endpoint_port_channels is returning a tuple of None")
    #         return (None, None)

    # def get_endpoint_port_channels(self, debug: bool = False) -> tuple[dict[dict], set]:
    #     '''
    #     Fetch all EGPs and their data
    #     returns a tuple of dict containing EPG infos and set of unique if_names
    #     '''
    #     # Download all of the interfaces
    #     # and store the data as tuples in a list
    #     if not debug:
    #         data: dict = {}
    #         port_channels = set([])
    #         endpoints = aci.Endpoint.get(self._apic)
    #         for ep in endpoints:
    #             ep_entry: dict = {}
    #             epg = ep.get_parent()
    #             app_profile = epg.get_parent()
    #             tenant = app_profile.get_parent()
    #             ep_entry["ip"] = ep.ip
    #             ep_entry["if_name"] = ep.if_name
    #             ep_entry["encap"] = ep.encap
    #             ep_entry["tenant_name"] = tenant.name
    #             ep_entry["app_profile_name"] = app_profile.name
    #             ep_entry["epg_name"] = epg.name
    #             data[ep.mac] = ep_entry
    #             port_channels.add(ep.if_name)
    #             children: list[Endpoint] = epg.get_children()
    #             for child in children:
    #                 print("child", child)
    #                 print("epg infos", child.name)
    #         return (data, port_channels)
    #     else:
    #         print("WARN: get_endpoint_port_channels is returning a tuple of None")
    #         return (None, None)

    # def get_pc_children(self, node_id, intf_id=None) -> set[str]:
    #     '''
    #     returns a dictionaries of Port Channels and their corresponding Node ID for
    #     a selected node_id
    #     '''
    #     pc_dict: dict = {}
    #     pc_name: str = None

    #     pod_list = []
    #     pods = aci.Pod.get(self._apic)
    #     for pod in pods:
    #         pod_list.append(pod.pod)

    #     for pod in pod_list:
    #         query_url = ('/api/mo/topology/pod-%s/node-%s/sys.json?query-target=subtree'
    #                      '&target-subtree-class=pcAggrIf&rsp-subtree=children&'
    #                      'rsp-subtree-class=pcRsMbrIfs' % (pod, node_id))  # removed pcRsLacpPolCons,l1RsL2IfPolCons,pcRtVpcConf,ethpmAggrIf as not needed
    #         error_message = 'Could not collect APIC data for switch %s.' % node_id
    #         port_channels = self._get_query(query_url, error_message)
    #         for pc in port_channels:
    #             print("port_channel", pc)
    #             pc_name = pc.get("pcAggrIf")["attributes"].get("name")
    #             pc_dict[pc_name] = node_id
    #     print("get_pc_children returning", pc_dict)
    #     return (pc_dict)

    def populate_port_channels(self, node_id, intf_id=None):
        pod_list = []
        pods = aci.Pod.get(self._apic)
        for pod in pods:
            pod_list.append(pod.pod)

        for pod in pod_list:
            query_url = ('/api/mo/topology/pod-%s/node-%s/sys.json?query-target=subtree'
                         '&target-subtree-class=pcAggrIf&rsp-subtree=children&'
                         'rsp-subtree-class=pcRsLacpPolCons,l1RsL2IfPolCons,pcRtVpcConf,ethpmAggrIf,pcRsMbrIfs' % (pod, node_id))
            error_message = 'Could not collect APIC data for switch %s.' % node_id
            port_channels = self._get_query(query_url, error_message)
            if intf_id is None:
                self._port_channels = port_channels
            else:
                self._port_channels = []
                for port_channel in port_channels:
                    for if_type in port_channel:
                        if port_channel[if_type]['attributes']['id'] == intf_id:
                            self._port_channels.append(port_channel)

    def populate_interfaces(self, node_id):
        pod_list = []
        pods = aci.Pod.get(self._apic)
        for pod in pods:
            pod_list.append(pod.pod)

        for pod in pod_list:
            query_url = ('/api/mo/topology/pod-%s/node-%s/sys.json?query-target=subtree'
                         '&target-subtree-class=l1PhysIf&rsp-subtree=children&'
                         'rsp-subtree-class=pcAggrMbrIf' % (pod, node_id))
            error_message = 'Could not collect APIC data for switch %s.' % node_id
            self._interfaces = self._get_query(query_url, error_message)

    def show_summary(self, node=None, intf_id=None):
        """
        show port-channel summary

        :param node: String containing the specific switch id. If none, all switches are used
        :param intf_id: String containing the specific interface id. If none, all interfaces are used
        :return: None
        """
        for node_id in self.get_node_ids(node):
            self.populate_interfaces(node_id)
            self.fetch_lacp_policies(node_id)

            self.populate_port_channels(node_id, intf_id)
            if not len(self._port_channels):
                print("No port channels in Switch: %s" % str(node_id))
                continue
            print("Switch: %s" % str(node_id))
            # print("Flags:  D - Down        P - Up in port-channel (members)")
            # print("        I - Individual  H - Hot-standby (LACP only)")
            # print("        s - Suspended   r - Module-removed")
            # print("        S - Switched    R - Routed")
            # print("        U - Up (port-channel)")
            # print("        M - Not in use. Min-links not met")
            # print("        F - Configuration failed")
            data = []
            for interface in self._port_channels:
                intf_attr = interface['pcAggrIf']['attributes']
                # if "frame" not in intf_attr['name'].lower():
                #     print("EXITING LOOP - not named 'FRAME'")
                #     break
                print("_port_channel loop: ", json.dumps(
                    interface, sort_keys=True, indent=4))
                name = intf_attr['id']
                if intf_attr['layer'] == 'Layer2':
                    name += "(S"
                else:
                    name += "(R"

                for child in interface['pcAggrIf']['children']:
                    if 'ethpmAggrIf' in child:
                        oper_attr = child['ethpmAggrIf']['attributes']
                        if oper_attr['operSt'] == 'up':
                            name += "U)"
                        elif intf_attr['suspMinlinks'] == 'yes':
                            name += "M)"
                        else:
                            name += "D)"
                        members = oper_attr['activeMbrs']
                        while ',unspecified,' in members:
                            members = members.replace(',unspecified,', ',')
                        members = members.replace(',unspecified', '')

                members += self._get_member_extension(interface)
                protocol = 'none'
                if intf_attr['pcMode'] in ['active', 'passive', 'mac-pin']:
                    protocol = 'lacp'
                data.append(
                    (int(intf_attr['id'][2:]), name, 'eth', protocol, members))
            data.sort(key=lambda tup: tup[0])
            headers = ['Group', 'Port channel',
                       'Type', 'Protocol', 'Member Ports']
            print(tabulate(data, headers=headers))

    def fetch_aci_node_lacp(self, node=None, debug: bool = False) -> dict:
        if not debug:
            lacp_infos = {}
            for node_id in self.get_node_ids(node):
                inspect_lacp: dict = self.fetch_lacp_policies(node_id, debug)
                lacp_infos[node_id] = inspect_lacp
            # print("lacp_infos", lacp_infos)
            # print("compare to ", fetch_aci_lacp_lacp_infos[node])
            return lacp_infos
        else:
            return fetch_aci_lacp_lacp_infos[node]

    def fetch_lacp_policies(self, node_id, debug: bool = False) -> list:
        if not debug:
            # check both pods for the node
            pod_list = []
            pods = aci.Pod.get(self._apic)
            for pod in pods:
                pod_list.append(pod.pod)

            for pod in pod_list:
                query_url = ('/api/mo/topology/pod-%s/node-%s/sys.json?query-target=subtree'
                             '&target-subtree-class=lacpIf&rsp-subtree=children&'
                             'rsp-subtree-class=l2RsEthIf,lacpAdjEp' % (pod, node_id))
                error_message = 'Could not collect APIC LACP data for switch %s.' % node_id
                lacp_policy = self._get_query(query_url, error_message)
                if len(lacp_policy) != 0:
                    return lacp_policy
        else:
            return  # fetch_lacp_policies_lacp_policy

# def main():
#     """
#     Main common routine for show interface description
#     :return: None
#     """
#     # Set up the command line options
#     creds = Credentials(['apic', 'nosnapshotfiles'],
#                         description=("This application replicates the switch "
#                                      "CLI command 'show interface fex'"))
#     creds.add_argument('-s', '--switch',
#                        type=str,
#                        default=None,
#                        help='Specify a particular switch id, e.g. "101"')
#     creds.add_argument('-i', '--interface',
#                        type=str,
#                        default=None,
#                        help='Specify a particular interface id, e.g. "po101"')
#     args = creds.get()

#     interface_collector = PortChannelCollector(args.url, args.login, args.password)

#     interface_collector.show_lacp(node=args.switch, intf_id=args.interface)

# if __name__ == '__main__':
#     try:
#         main()
#     except KeyboardInterrupt:
#         pass
