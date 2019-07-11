from django.shortcuts import render
from rest_framework_mongoengine import generics
from rest_framework import generics
from .serializers import deviceSerializer,deviceListSerializer
from QoSmonitor.models import * 
from napalm import get_network_driver 
from rest_framework import status
from rest_framework.response import Response



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

