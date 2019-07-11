from django.urls import path 
from .views import *
urlpatterns = [
    path('add',AddDevice.as_view(), name = "add-device"),
    path('devices',DeviceList.as_view(), name = "device-list"),
]
app_name = 'QoSAPI'