import json


def output_references_device(device):
    device_dct = json.loads(device.to_json(indent=2))
    del(device_dct['_id'])
    device_dct["interfaces"] = [
    json.loads(interface.to_json(indent=2)) for interface in device.interfaces]
    for interf in device_dct["interfaces"]:
        del(interf['_id'])

    return json.dumps(device_dct,indent=4)
    



def output_references_link(link):
        link_dct = json.loads(link.to_json(indent=2))
        del (link_dct['_id'])
        link_dct["from_device"] = json.loads(output_references_device_brief(link.from_device))
        link_dct["to_interface"] = json.loads(link.to_interface.to_json(indent=2))
        del (link_dct["to_interface"]['_id'])
        link_dct["from_interface"] = json.loads(link.from_interface.to_json(indent=2))
        del (link_dct["from_interface"]['_id'])
        link_dct["to_device"] = json.loads(output_references_device_brief(link.to_device))

        return json.dumps(link_dct, indent=4)


def output_references_topology(topology):
    topology_dct = json.loads(topology.to_json(indent=2))
    del (topology_dct['_id'])
    topology_dct["devices"] = [
        json.loads(output_references_device(device)) for device in topology.devices
    ]
    topology_dct["links"] = [
        json.loads(output_references_link(link)) for link in topology.links
    ]

    return json.dumps(topology_dct, indent=4)

def output_references_topology_brief(topology):
    topology_dct = json.loads(topology.to_json(indent=2))
    del (topology_dct['_id'])
    del (topology_dct['devices'])
    del (topology_dct['links'])

    return json.dumps(topology_dct, indent=4)


def output_references_device_brief(device):

    device_dct = json.loads(device.to_json(indent=2))
    del(device_dct['_id'])
    device_dct["interfaces"] = [
    json.loads(interface.to_json(indent=2)) for interface in device.interfaces]
    del(device_dct['interfaces'])

    return json.dumps(device_dct,indent=4)

