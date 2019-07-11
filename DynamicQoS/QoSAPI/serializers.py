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

	def validate(self,value):
					management = value['management']
					addr = management["management_address"]
					user = management["username"]
					passwd = management['password']
					driver = get_network_driver("ios")
					device = driver(addr,user,passwd)
					try:
						device.open()
						device.close()
						return value 
					except Exception as e :
						sr.ValidationError(e)

	class Meta:
		model = device 
		fields = ["management"]



class interfaceSerializer(serializers.DocumentSerializer):
	class Meta:
		model = interface 
		fields = "__all__"

class deviceListSerializer(serializers.DocumentSerializer):
	management = accessSerializer(many = False)
	class Meta:
		model = device
		fields = "__all__"
