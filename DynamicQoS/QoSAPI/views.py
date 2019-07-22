import json
from netaddr import * 
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
		topology_qs = topology.objects(topology_name = topo_name)
		if len(topology_qs) == 0 :
			serializer.save()
		else:
			raise sr.ValidationError("topology name {} exists ! try another one.".format(topo_name))


class AddDevice(generics.CreateAPIView):
	serializer_class = deviceSerializer
	
	def perform_create(self, serializer):
		addr = self.request.data.get("management.management_address")
		user = self.request.data.get("management.username")
		passwd = self.request.data.get("management.password")
		driver = get_network_driver("ios")
		topo_name = self.request.data.get("topology_name")
		topology_qs = topology.objects(topology_name = topo_name)
		if len(topology_qs) == 0:
			raise sr.ValidationError("topology doesn't exists")
		else :
			device = driver(addr,user,passwd,timeout = 5)
			fqdn = None
			device_list = topology_qs[0].devices
			device.open()
			fqdn = device.get_facts()['fqdn']
			device.close()
			device_serializer = serializer.save(hostname = fqdn)
			new_device = device.objects.get(id = device_serializer.id)
			other_list = [new_device]
			for device_cursor in device_list:
				other_list.append(device.objects.get(id = device_cursor.id))
			topology_qs[0].update(set__devices = other_list)
  
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

class preapare_environment(generics.CreateAPIView):
	serializer_class = preapare_envSerializer
	queryset = "Nothing to do here it is out of models"
	def get(self,request):
		return Response("Specify the topology to prepare the envirement")

	def create(self,serializer):
		topology_name = self.request.data.get("topology")
		try:
			topology_exist = topology.objects.get(topology_name = topology_name)
		except:
			raise sr.ValidationError("Topology '{}' doesn't exist".format(topology_name))
		try :
			topology_exist.configure_ntp()
			configure_ntp.configure_scp()
			configure_ntp.configure_snmp()
		except Exception as e:
			raise sr.ValidationError("ERROR : {}".format(e))


class discover_network(generics.CreateAPIView):
	serializer_class =  discover_networkSerializer
	queryset = "Nothing to do here it is out of models"
	def get(self,request):
		return Response("please specify the topology to discover")
	def create(self,serializer):
		topology_name = self.request.data.get("topology")
		try:
			topology_exist = topology.objects.get(topology_name = topology_name)
		except:
			raise sr.ValidationError("Topology '{}' doesn't exist".format(topology_name))

		try:
			topology_exist.get_networks()
		except Exception as e:
			raise sr.ValidationError("ERROR : {}".format(e))

		try:
			topology_exist.create_links()
		except Exception as e:
			raise sr.ValidationError("ERROR : {}".format(e))

		return Response("Discovery is finish successfully")



class configure_monitoring(generics.CreateAPIView):
	serializer_class =  configure_monitoringSerializer
	queryset = "Nothing to do here it is out of models"
	def get(self,request):
		return Response("please specify the topology name and destination of collector")
	def create(self,serializer):
		collector = self.request.data.get("destination")
		topology_name = self.request.data.get("topology")
		try:
			IPAddress(collector)
		except:
			raise sr.ValidationError(" '{}' is not a valide ip address".format(collector))
		try:
			topology_exist = topology.objects.get(topology_name = topology_name)
		except:
			raise sr.ValidationError("Topology '{}' doesn't exist".format(topology_name)) 
		if topology_exist.monitoring_enabled == True:
			raise sr.ValidationError("Topology '{}' is already configured".format(topology_name))

		"""monitors = topology_exist.get_monitors()
		for monitor in monitors:
			try:
				monitor.configure_netflow(destination = collector)
			except Exception as e:
				raise sr.ValidationError("ERROR : {}".format(e))"""
				
		for monitor in topology_exist.devices:
			try:
				monitor.configure_netflow(destination = collector)
			except Exception as e :
				raise sr.ValidationError("ERROR : {}".format(e))


		topology_exist.monitoring_enabled = True
		topology_exist.update(set__monitoring_enabled = True)
		return Response("Monitoring is configured successfully")

class start_monitoring(generics.CreateAPIView):
	serializer_class =  start_monitoringSerializer
	queryset = "Nothing to do here it is out of models"
	def get(self,request):
		return Response("please specify the topology to start monitoring")
	def create(self,serializer):
		topology_name = self.request.data.get("topology")
		try:
			topology_exist = topology.objects.get(topology_name = topology_name)
		except:
			raise sr.ValidationError("Topology '{}' doesn't exist".format(topology_name))

		if topology_exist.monitoring_activated == True:
			raise sr.ValidationError("Topology '{}' is already monitored".format(topology_name))


		# TODO : Block here to start the monitoring

		topology_exist.monitoring_activated = True
		topology_exist.update(set__monitoring_activated = True)
		return Response("Monitoring is starting successfully")





