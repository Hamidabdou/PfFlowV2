from rest_framework_mongoengine import serializers 
from QoSmonitor.models import * 

class accessSerializer(serializers.EmbeddedDocumentSerializer):
	class Meta:
		model = access
		fields = "__all__"
		

class deviceSerializer(serializers.DocumentSerializer):
	management = accessSerializer(many = False)
	class Meta:
		model = device 
		fields = "__all__"

