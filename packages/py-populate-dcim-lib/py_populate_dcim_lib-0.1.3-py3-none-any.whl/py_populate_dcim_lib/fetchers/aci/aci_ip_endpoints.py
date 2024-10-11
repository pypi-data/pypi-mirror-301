#!/usr/bin/env python
import re
from etherflow_acitoolkit import Session


class IpEndpointCollector(object):
    """
    Search for a physical endpoint name by IP
    """

    @classmethod
    def __init__(self, session: Session):
        # Login to APIC
        self._apic = session

    @classmethod
    def _get_query(self, query_url, error_msg) -> list:
        resp = self._apic.get(query_url)
        if not resp.ok:
            print(error_msg)
            print(resp.text)
            return []
        return resp.json()['imdata']

    def fetch_aci_endpoint_by_ip(self, ip: str) -> tuple[str]:
        """
        Search for an Endpoint stored in ACI by IP
        and return a tuple containing
        1. the ethernet port name it plugs into
        2. the node ID
        3. the FEX ID if it exists
        4. the VPC ID if it exists
        5. the MAC address
        """
        (fvcep_dn, fvcep_mac) = self._fetch_aci_fvCEp_by_ip(ip)
        if fvcep_dn:
            fvRsCEpToPathEp_tdn: str = self._fetch_aci_fvRsCEpToPathEp_by_dn(
                fvcep_dn)
            ethernet_location = re.search(
                "(?<=\\[eth)(.*?)(?=\\])", fvRsCEpToPathEp_tdn)
            node_id = re.search(
                "(?<=/paths-)([0-9]*)(?<!/)", fvRsCEpToPathEp_tdn
            )
            fex_id = re.search(
                "(?<=/extpaths-)([0-9]*)(?<!/)", fvRsCEpToPathEp_tdn
            )
            bracketed_id: re.Match[str] | None = re.search(
                "(?<=\\[)(.*?)(?=\\])", fvRsCEpToPathEp_tdn)
            if bracketed_id:
                if "vpc" in bracketed_id.group(0).lower():
                    node_id = re.search(
                        "(?<=\\/protpaths-)(\\d*)(-{0,1}\\d*)*(?<!\\/)", fvRsCEpToPathEp_tdn
                    )
                    # return VPC data in this case
                    return (None, node_id.group(0), None, bracketed_id.group(0), fvcep_mac)
            if fex_id:
                # return eth ports and FEX ID in this case
                return (ethernet_location.group(0), node_id.group(0), fex_id.group(0), None, fvcep_mac)
            elif ethernet_location:
                # return only ethernet location and node ID in this case
                return (ethernet_location.group(0), node_id.group(0), None, None, fvcep_mac)
            # else
            return (None, None, None, None, None)
        else:
            print("WARN: did not find an endpoint for IP ", ip)
            return (None, None, None, None, None)

    @classmethod
    def _fetch_aci_fvCEp_by_ip(self, ip: str):
        query_url = (
            '/api/node/class/fvCEp.json?rsp-subtree=full&rsp-subtree-include=required&rsp-subtree-filter=eq(fvIp.addr,"%s")' % (ip))
        error_message = 'Could not collect APIC fvCEp data for  %s.' % ip
        fvCEp_info = self._get_query(query_url, error_message)
        fvcep_dn = fvCEp_info[0].get('fvCEp').get('attributes').get('dn')
        fvcep_mac = fvCEp_info[0].get('fvCEp').get('attributes').get('mac')
        return (fvcep_dn, fvcep_mac)

    @classmethod
    def _fetch_aci_fvRsCEpToPathEp_by_dn(self, fvcep_dn: str) -> str:
        """
        Given an fvCEP dn from ACI, search for fvRsCEpToPathEp
        :return: the unique name of a connection endpoint that describes a phsysical location
        """
        query_url = '/api/node/mo/%s.json?query-target=subtree&target-subtree-class=fvRsCEpToPathEp' % (
            fvcep_dn)
        error_message = 'Could not collect APIC fvRsCEpToPathEp data for  %s.' % fvcep_dn
        fvRsCEpToPathEp_info = self._get_query(query_url, error_message)
        tDn: str = fvRsCEpToPathEp_info[0]['fvRsCEpToPathEp']['attributes']['tDn']
        return tDn
