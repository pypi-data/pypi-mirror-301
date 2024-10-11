#!/usr/bin/env python
import json
import etherflow_acitoolkit as aci
from etherflow_acitoolkit import Session
from tabulate import tabulate
from ...debug.stand_in_objects import aci_endpoint_vpcs_vpcs, aci_endpoint_vpcs_data, get_vpc_children_vpc_children


class VpcCollector(object):
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

    def get_endpoint_vpcs(self, stringfilters: list[str] = None, debug: bool = False):
        # Download all of the interfaces
        # and store the data as tuples in a list
        if not debug:
            data = []
            vpcs = set([])
            endpoints = aci.Endpoint.get(self._apic)
            for ep in endpoints:
                epg = ep.get_parent()
                app_profile = epg.get_parent()
                tenant = app_profile.get_parent()
                if stringfilters:
                    if any(x.upper() in ep.if_name.upper() for x in stringfilters):
                        if 'dmz'.upper() not in ep.if_name.upper():  # do not include DMZ
                            data.append((ep.mac, ep.ip, ep.if_name, ep.encap,
                                        tenant.name, app_profile.name, epg.name))
                            vpcs.add(ep.if_name)
                else:
                    data.append((ep.mac, ep.ip, ep.if_name, ep.encap,
                                tenant.name, app_profile.name, epg.name))
            return (data, vpcs)
        else:
            return (aci_endpoint_vpcs_data, aci_endpoint_vpcs_vpcs)

    @classmethod
    def _display_endpoint_vpcs(self, ep_vpcs):
        # Display the data downloaded
        print(tabulate(ep_vpcs, headers=["MACADDRESS", "IPADDRESS", "INTERFACE",
                                         "ENCAP", "TENANT", "APP PROFILE", "EPG"]))

    def get_vpc_children(self, vpc_set: set, debug: bool = False) -> dict[set]:
        if not debug:
            vpc_children = {}

            for vpc_name in vpc_set:
                vpc_included_nodes = []
                query_url = ('/api/node/mo/uni/infra/funcprof/accbundle-%s.json?rsp-subtree-include=full-deployment'
                             '&target-path=AccBaseGrpToEthIf' % (vpc_name))
                error_message = 'Could not collect APIC VPC data for  %s.' % vpc_name
                vpc_info = self._get_query(query_url, error_message)
                # print("queried", query_url, "with result:", json.dumps(vpc_info[0]['infraAccBndlGrp']['children'], indent=4)) #pconsNodeDeployCtx
                for children in vpc_info[0]['infraAccBndlGrp']['children']:
                    vpc_included_nodes.append(
                        children['pconsNodeDeployCtx']['attributes']['nodeId'])

                vpc_children[vpc_name] = vpc_included_nodes
            return vpc_children
        else:
            return get_vpc_children_vpc_children
