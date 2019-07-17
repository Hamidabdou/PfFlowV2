from rest_framework_mongoengine import serializers 
from QoSmonitor.models import * 
from rest_framework import serializers as sr
from napalm import get_network_driver

class accessSerializer(serializers.EmbeddedDocumentSerializer):
	class Meta:
		model = access
		fields = "__all__"
		

class deviceSerializer(serializers.DocumentSerializer):
	management = accessSerializer(many = False)
	topology_name = sr.CharField()
	def validate(self,value):
					management = value['management']
					addr = management["management_address"]
					user = management["username"]
					passwd = management['password']
					driver = get_network_driver("ios")
					device = driver(addr,user,passwd,timeout = 10)
					try:
						device.open()
						device.close()
						return value 
					except Exception as e :
						raise sr.ValidationError(e)
					
	class Meta:
		model = device
		fields = ["management","topology_name"]



class topologySerializer(serializers.DocumentSerializer):
	class Meta:
		model = topology
		fields = ["topology_name","topology_desc"]

class deviceListSerializer(serializers.DocumentSerializer):
	management = accessSerializer(many = False)
	class Meta:
		model = device
		fields = "__all__"





