from django.urls import path 
from .views import *

urlpatterns = [
    path('add-device',AddDevice.as_view(), name = "add-device"),
    path('add-topology', AddTopology.as_view(), name = "add-topology"), 
    path('topology',TopologyByName.as_view(), name = "topology-by-name"),
    path('topologiesbrief',ListTopologiesBrief.as_view(), name = "topologies"),
    path('devicesbrief',ListDevicesBrief.as_view(), name = "devices"),
    path('interfacesbrief',ListInterfacesBrief.as_view(), name = "interfaces"),
    path('flowtable',FlowTable.as_view(), name = "flowtable"),
    path('flowtabletworates', FlowTableTwoRates.as_view(), name="flowtabletworates"),
]


app_name = 'APIv1'
