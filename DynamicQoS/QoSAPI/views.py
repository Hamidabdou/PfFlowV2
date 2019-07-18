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
from rest_framework import serializers as sr


class AddTopology(generics.CreateAPIView):
    serializer_class = topologySerializer
    queryset = topology.objects()

    def perform_create(self, serializer):
        topo_name = self.request.data.get("topology_name")
        topology_qs = topology.objects(topology_name=topo_name)
        if len(topology_qs) == 0:
            serializer.save()
        else:
            raise sr.ValidationError("topology name {} exists ! try another one.".format(topo_name))


class AddDevice(generics.CreateAPIView):
    serializer_class = deviceSerializer

    def perform_create(self, serializer):
        print(serializer)
        addr = self.request.data.get("management.management_address")
        user = self.request.data.get("management.username")
        passwd = self.request.data.get("management.password")
        driver = get_network_driver("ios")
        topo_name = self.request.data.get("topology_name")
        topology_qs = topology.objects(topology_name=topo_name)
        if len(topology_qs) == 0:
            raise sr.ValidationError("topology doesn't exists")
        else:
            device = driver(addr, user, passwd, timeout=5)
            fqdn = None
            device_list = topology_qs[0].devices
            device.open()
            fqdn = device.get_facts()['fqdn']
            device.close()
            device_serializer = serializer.save(hostname=fqdn)
            new_device = device.objects.get(id=device_serializer.id)
            other_list = [new_device]
            for device_cursor in device_list:
                other_list.append(device.objects.get(id=device_cursor.id))
            topology_qs[0].update(set__devices=other_list)


class TopologyByName(APIView):

    def get(self, request):

        if len(request.query_params) == 0:
            result = {'topologies': []}
            topologies = topology.objects()
            for topo in topologies:
                result['topologies'].append(json.loads(output_references_topology_brief(topo)))
            return Response(result)
        else:
            topology_name = request.query_params.get("name")
            if topology_name == None:
                return Response({'error': 'specify a correct query'})
            topologies = topology.objects(topology_name=topology_name)
            if len(topologies) == 0:
                return Response({'error': 'topology does not exists'})
            else:

                for topo in topologies:
                    result = json.loads(output_references_topology(topo))
                return Response(result)


class StatisticsTimed(APIView):
    def get(self, request):

        if len(request.query_params) == 0:
            result = {'topologies': []}
            return Response(result)
        else:
            topology_name = request.query_params.get("topology")
            start_time = request.query_params.get("start_time")
            end_time = request.query_params.get("end_time")
            if topology_name == None:
                return Response({'error': 'specify a correct query'})
            topologies = topology.objects(topology_name=topology_name)
            flows = topologie
            if len(topologies) == 0:
                return Response({'error': 'topology does not exists'})
            else:

                for topo in topologies:
                    result = json.loads(output_references_topology(topo))
                return Response(result)
