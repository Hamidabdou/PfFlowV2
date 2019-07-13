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
from .utils import output_references_topology, output_references_topology_brief





class AddTopology(generics.CreateAPIView):
	serializer_class = topologySerializer

class AddDevice(generics.CreateAPIView):
	serializer_class = deviceSerializer
	
	def perform_create(self, serializer):
		addr = self.request.data.get("management.management_address")
		user = self.request.data.get("management.username")
		passwd = self.request.data.get("management.password")
		driver = get_network_driver("ios")
		print(self.request.data)
		device = driver(addr,user,passwd,timeout = 5)
		fqdn = None 
		device.open()
		fqdn = device.get_facts()['fqdn']
		device.close()
		serializer.save(hostname = fqdn)

"""class DeviceList(generics.ListAPIView):
    serializer_class = deviceListSerializer
    def get_queryset(self):
        queryset = device.objects.all()
        return queryset"""


class TopologyList(APIView):
    def get(self, request):
        result={'topologies':[]}
        topologies = topology.objects()
        for topo in topologies:
            result['topologies'].append(json.loads(output_references_topology(topo)))
        return Response(result)
  
  
class TopologyByName(APIView):

    def get(self,request):

        if len(request.query_params)==0:
            result = {'topologies': []}
            topologies = topology.objects()
            for topo in topologies:
                result['topologies'].append(json.loads(output_references_topology_brief(topo)))
            return Response(result)
        else:
            topology_name = request.query_params.get("name")
            if topology_name==None:
                return Response({'error': 'specify a correct query'})
            topologies = topology.objects(topology_name=topology_name)
            if len(topologies)==0:
                return Response({'error': 'topology does not exists'})
            else:

                for topo in topologies:
                    result = json.loads(output_references_topology(topo))
                return Response(result)


