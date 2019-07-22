from django.urls import path 
from .views import *

urlpatterns = [
    path('add-device',AddDevice.as_view(), name = "add-device"),
    path('add-topology', AddTopology.as_view(), name = "add-topology"), 
    path('topology',TopologyByName.as_view(), name = "topology-by-name"),
    path('preapare-env', preapare_environment.as_view(),name = "preapare-environment")
    path('discover-network',discover_network.as_view(),name = "discover-network"),
    path('configure-monitoring',configure_monitoring.as_view(),name = "configure-monitoring"),
    path('start-monitoring',start_monitoring.as_view(),name = "start-monitoring"),
]

app_name = 'APIv1'