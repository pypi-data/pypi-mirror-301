from argparse import Namespace
from hpOneView.oneview_client import OneViewClient
from hpOneView.exceptions import HPOneViewException
from ...debug.stand_in_objects import filtered_oneview_example, oneview_macs_example
from hpOneView.resources.networking.interconnects import Interconnects

def poll_one_view(args: Namespace) -> tuple[frozenset, dict[dict]]:
    if not args.debug:
        print("INFO: Connecting to OneView...")
        oneview_client = OneViewClient.from_environment_variables()
        print("INFO: Connected to OneView!")

        # Get all interconnects relevant info
        # returns nested dictionary
        macs = []
        dupmacs = []
        oneview_infos = {}
        try:
            interconnects: list[Interconnects] = oneview_client.interconnects.get_all()#filter="\"'name'='OneViewSDK Test FC Network'\""
            for ic in interconnects:
                # build a dictionary of our needed values
                print("entire oneview ic", ic)
                icdata = {}
                icdata["id"] = ic.get("id")
                for addrObj in ic.get("ipAddressList"):
                    if "Ipv6" in addrObj.get("ipAddressType"):
                        icdata["ipv6Addr"] = addrObj.get("ipAddress")
                    elif "Ipv4" in addrObj.get("ipAddressType"):
                        icdata["ipv4Addr"] = addrObj.get("ipAddress")
                icdata["applianceName"] = ic.get("applianceName")
                icdata["enclosureName"] = ic.get("enclosureName")
                icdata["bayNumber"] = ic.get("bayNumber")
                icdata["serialNumber"] = ic.get("serialNumber")
                mac = ic.get("interconnectMAC", "FF:FF:FF:FF:FF:FF")

                if (
                    mac not in macs
                    and mac != "FF:FF:FF:FF:FF:FF"
                    and mac != "00:00:00:00:00:00"
                ):
                    # append the dictionary into the output dictionary
                    oneview_infos[mac] = icdata
                    # append the mac to our hash table
                    macs.append(mac)
                else:
                    # MAC addresses should always be unique
                    # so any duplicates or defaults get thrown into their own object (or thrown away)
                    dupmacs.append((mac, icdata))

        except HPOneViewException as e:
            print("poll_one_view found an exception:", e.msg)
        
        macs = frozenset(macs)
        assert len(macs) == len(oneview_infos)

    else:
        print("Debug enabled - not polling OneView API")
        macs = oneview_macs_example
        oneview_infos = filtered_oneview_example
    return (macs, oneview_infos)
