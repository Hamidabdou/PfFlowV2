from django.shortcuts import render
from rest_framework_mongoengine import generics
from rest_framework import generics
from .serializers import deviceSerializer
from QoSmonitor.models import * 

class AddDevice(generics.CreateAPIView):
	serializer_class = deviceSerializer



