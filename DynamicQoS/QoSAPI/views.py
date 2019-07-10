import json

from django.shortcuts import render
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework_mongoengine import generics
from rest_framework import generics

from .utils import output_references_topology
from .serializers import deviceSerializer
from QoSmonitor.models import *

class AddDevice(generics.CreateAPIView):
	serializer_class = deviceSerializer




class MyOwnView(APIView):
	def get(self, request):
		result={'topologies':[]}
		topologies = topology.objects()
		for topo in topologies:
			print('....')
			result['topologies'].append(json.loads(output_references_topology(topo)))




		return Response(result)

