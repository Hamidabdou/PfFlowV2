from django.urls import path 
from .views import *

urlpatterns = [
    path('add-device',AddDevice.as_view(), name = "add-device"),
    path('add-topology', AddTopology.as_view(), name = "add-topology"), 
    path('topology',TopologyByName.as_view(), name = "topology-by-name"),

]
app_name = 'APIv1'
