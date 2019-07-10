import json


def output_references_device(device):

	device_dct = json.loads(device.to_json(indent=2))
	device_dct["interfaces"] = [
    json.loads(interface.to_json(indent=2)) for interface in device.interfaces
  ]

	return json.dumps(device_dct,indent=4)

def output_references_topology(topology):

	topology_dct = json.loads(topology.to_json(indent=2))
	topology_dct["devices"] = [
    json.loads(output_references_device(device)) for device in topology.devices
  ]

	return json.dumps(topology_dct,indent=4)