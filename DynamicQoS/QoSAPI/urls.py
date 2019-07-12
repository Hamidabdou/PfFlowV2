from django.urls import path 

from .views import AddDevice, TopologyList

urlpatterns = [
    path('add',AddDevice.as_view(), name = "add-device"),
    path('topologies',TopologyList.as_view(), name = "topologies"),
]
app_name = 'QoSAPI'