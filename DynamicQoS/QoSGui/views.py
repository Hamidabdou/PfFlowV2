import json
import os

from django.core.files import File
from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from mongoengine import *
from django.shortcuts import render, redirect
from QoSmonitor.models import *
# Create your views here.

from QoSGui.forms import *

from QoSmonitor.models import topology

from DynamicQoS.settings import MEDIA_ROOT

from QoSmonitor.utils import check_if_exists


@login_required(login_url='/login/')
def home(request):
    ctx = {}
    return render(request,'home.html',context=ctx)


def drag_drop(request,topo_id):
    print(os.path.isfile(str(MEDIA_ROOT[0]) + "/topologies/" + str(topo_id) + ".json"))
    if os.path.isfile(str(MEDIA_ROOT[0]) + "/topologies/" + str(topo_id) + ".json"):
        with open(str(MEDIA_ROOT[0]) + "/topologies/" + str(topo_id) + ".json", 'r') as file:
            data = file.read().replace('\n', '')
            print(data)
            JsonFile = GetJsonFile(initial={'Text': data})
    else:

        JsonFile = GetJsonFile(initial={'Text': """{ "class": "go.GraphLinksModel",
                   "copiesArrays": true,
                   "copiesArrayObjects": true,
                   "linkFromPortIdProperty": "fromPort",
                   "linkToPortIdProperty": "toPort",
                   "nodeDataArray": [],
                   "linkDataArray": []}"""})

    ctx = {'json': JsonFile, 'id': topo_id}
    return render(request, 'dragndrop.html', context=ctx)


def add_topology(request):
    TopoForm = AddTopologyForm(request.POST)
    if TopoForm.is_valid():
        tp = topology(topology_name=request.POST['Name'], topology_desc=request.POST['TopologyDesc'])
        tp.save()
    return HttpResponseRedirect(reverse('Topologies', kwargs={}))

def topologies(request):
    TopoForm = AddTopologyForm()
    topologies = topology.objects
    ctx = {'topology':TopoForm,'topologies':topologies}
    return render(request,'draw.html',context = ctx)

# def DrawTopology(request,topo_id):
#     print(os.path.isfile(str(MEDIA_ROOT[0]) + "/topologies/" + str(topo_id) + ".json"))
#     if os.path.isfile(str(MEDIA_ROOT[0]) + "/topologies/" + str(topo_id) + ".json"):
#         with open(str(MEDIA_ROOT[0]) + "/topologies/" + str(topo_id) + ".json", 'r') as file:
#             data = file.read().replace('\n', '')
#             print(data)
#             JsonFile = GetJsonFile(initial={'Text': data})
#     else:
#
#         JsonFile = GetJsonFile(initial={'Text': """{ "class": "go.GraphLinksModel",
#                 "copiesArrays": true,
#                 "copiesArrayObjects": true,
#                 "linkFromPortIdProperty": "fromPort",
#                 "linkToPortIdProperty": "toPort",
#                 "nodeDataArray": [],
#                 "linkDataArray": []}"""})
#     ctx = {'json':JsonFile,'id':topo_id}
#     return render(request,'dragndrop.html',context=ctx)


def save_json_topology(request,topo_id):
    JsonFile = GetJsonFile(request.POST)
    if JsonFile.is_valid:
        topology_json=request.POST['Text']
        data = json.loads(topology_json)
        file_url = (str(MEDIA_ROOT[0]) + "/topologies/" + str(topo_id) + ".json")
        with open(file_url, "w") as f:
            myfile = File(f)
            myfile.write(request.POST['Text'])

        topology_ins=topology.objects.get(id=topo_id)


        # for device in data['nodeDataArray']:
        #     """
        #        getting nodes data
        #
        #     """
        #     if not device['category'] == 'cloud':
        #
        #         try:
        #             location = device['Location']
        #         except KeyError:
        #             location = ''
        #         try:
        #             address = device['Address']
        #         except KeyError:
        #             address = ''
        #
        #         try:
        #             username = device['Username']
        #         except KeyError:
        #             username = ''
        #         try:
        #             password = device['Password']
        #         except KeyError:
        #             password = ''
        #         try:
        #             secret = device['Secret']
        #         except KeyError:
        #             secret = ''
        #
        #         """
        #         creating the devices
        #         """
        #         print(address+' '+location+' '+username+' '+password+' '+secret)
        #

    return HttpResponseRedirect(reverse('Home', kwargs={}))
