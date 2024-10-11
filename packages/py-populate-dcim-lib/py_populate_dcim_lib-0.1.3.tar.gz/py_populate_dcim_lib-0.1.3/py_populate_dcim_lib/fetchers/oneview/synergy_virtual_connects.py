from argparse import Namespace
import os
import csv


def format_one_view_data(args: Namespace) -> tuple[dict, frozenset]:
    one_view_lacp_data = {}
    one_view_macs: set = set([])
    csv_file_path = os.environ.get('ONEVIEW_CSV_PATH', 'fetchers/oneview/OneView Synergy LACP Port ID Common Mapping.csv')
    
    with open(csv_file_path, newline='') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            # trim out unused data
            row.pop("lacp_port_hex")
            row.pop("aggregator_mac")
            row.pop("channel_group")
            model = row.pop("device_model")
            composer = row.pop("source_composer")
            # if row.get("switch_bay") == '6':
            #     # ignore rear bay 6 because it is redundant to rear bay 3 from LACP's perspective
            #     continue
            mac: str = row.get("lacp_mac")
            one_view_macs.add(mac.upper())
            one_view_lacp_data[mac.upper()] = one_view_lacp_data.get(mac.upper(), {})
            one_view_lacp_data[mac.upper()]["device_model"] = model
            one_view_lacp_data[mac.upper()]["source_composer"] = composer
            one_view_lacp_data[mac.upper()]["Bay " + row.get("switch_bay")] = one_view_lacp_data.get(mac.upper()).get("Bay " + row.get("switch_bay"), {})
            one_view_lacp_data[mac.upper()]["Bay " + row.get("switch_bay")]["LACP " + row.get("lacp_port_decimal")] = row
    return (one_view_lacp_data, one_view_macs)

def oneview_lacp_port_location_map() -> dict:
    '''
    returns a dictionary mapping LACP port numbers to standard port locations
    '''
    lacp_port_loc = {}
    csv_file_path = os.environ.get('ONEVIEW_CSV_PATH', 'fetchers/oneview/OneView Synergy LACP Port ID Common Mapping.csv')
    
    with open(csv_file_path, newline='') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            if not lacp_port_loc.get(row.get("device_model")):
                lacp_port_loc[row.get("device_model")] = {}
            if row.get("lacp_port_decimal") not in lacp_port_loc[row.get("device_model")]:
                lacp_port_loc[row.get("device_model")][row.get("lacp_port_decimal")] = row.get("port_location")
    return lacp_port_loc


def populate_pair_oneview_synergy_data(oneview_lacp_data: dict, pairs: dict) -> dict:
    ov_lacp_port_locs = oneview_lacp_port_location_map()

    for cable in pairs:
        pairs[cable]['oneView']['model'] = oneview_lacp_data[pairs[cable]['oneView']['sysId'].upper()]['device_model']
        lacp_port_id = pairs[cable]['oneView']['port']
        pairs[cable]['oneView']['portLoc'] = ov_lacp_port_locs[pairs[cable]['oneView']['model']][lacp_port_id]
        # to get source frame, we can inspect oneview_lacp_data for its port_location to determine if it should come from bay 3 or 6
        # once determined, we can populate the correct source_frame below
        pairs[cable]['oneView']['composer'] = oneview_lacp_data[pairs[cable]['oneView']['sysId'].upper()]['source_composer']
        port_loc: str = oneview_lacp_data[pairs[cable]['oneView']['sysId'].upper()]["Bay 3"]["LACP " + lacp_port_id]["port_location"] # data for both bay 3 and 6 contain same port location
        if port_loc.startswith("1"):
            pairs[cable]['oneView']['frame'] = oneview_lacp_data[pairs[cable]['oneView']['sysId'].upper()]["Bay 6"]["LACP " + lacp_port_id]["source_frame"]
        elif port_loc.startswith("0"):
            pairs[cable]['oneView']['frame'] = oneview_lacp_data[pairs[cable]['oneView']['sysId'].upper()]["Bay 3"]["LACP " + lacp_port_id]["source_frame"]        
    return pairs
