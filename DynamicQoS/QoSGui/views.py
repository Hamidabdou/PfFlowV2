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




@login_required(login_url='/login/')
def home(request):
    ctx = {}
    return render(request,'home.html',context=ctx)


def drag_drop(request,topo_id):


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
    return HttpResponseRedirect(reverse('Home', kwargs={}))

def topologies(request):
    TopoForm = AddTopologyForm()
    topologies = topology.objects
    ctx = {'topology':TopoForm,'topologies':topologies}
    return render(request,'draw.html',context = ctx)

def DrawTopology(request,topo_id):

    JsonFile = GetJsonFile(initial={'Text': """{ "class": "go.GraphLinksModel",
            "copiesArrays": true,
            "copiesArrayObjects": true,
            "linkFromPortIdProperty": "fromPort",
            "linkToPortIdProperty": "toPort",
            "nodeDataArray": [],
            "linkDataArray": []}"""})
    ctx = {'json':JsonFile,'id':topo_id}
    return render(request,'dragndrop.html',context=ctx)

def save_json_topology(request,topo_id):
    JsonFile = GetJsonFile(request.POST)
    if JsonFile.is_valid:
        topology_json=request.POST['Text']
        print(topology_json)

    return HttpResponseRedirect(reverse('Home', kwargs={}))
