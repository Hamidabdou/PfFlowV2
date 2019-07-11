import json

from django.shortcuts import render
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework_mongoengine import generics
from rest_framework import generics

from .serializers import *
from QoSmonitor.models import * 
from napalm import get_network_driver 
from rest_framework import status
from rest_framework.response import Response
from .utils import output_references_topology

class AddDevice(generics.CreateAPIView):
	serializer_class = deviceSerializer
	
	def perform_create(self, serializer):
		addr = self.request.data.get("management.management_address")
		user = self.request.data.get("management.username")
		passwd = self.request.data.get("management.password")
		driver = get_network_driver("ios")
		device = driver(addr,user,passwd)
		device.open()
		serializer.save(hostname = device.get_facts()['fqdn'])
		device.close()

class DeviceList(generics.ListAPIView):
	serializer_class = deviceListSerializer
	def get_queryset(self):
		queryset = device.objects.all()
		return queryset


class MyOwnView(APIView):
	def get(self, request):
		result={'topologies':[]}
		topologies = topology.objects()
		for topo in topologies:
			print('....')
			result['topologies'].append(json.loads(output_references_topology(topo)))




		return Response(result)

