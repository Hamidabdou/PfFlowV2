from django.urls import path 

from .views import *

urlpatterns = [
    path('add',AddDevice.as_view(), name = "add-device"),
    path('topologies',TopologyByName.as_view(), name = "topologies"),
]
app_name = 'QoSAPI'