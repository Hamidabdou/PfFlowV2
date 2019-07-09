from django.urls import path 
from .views import AddDevice
urlpatterns = [
    path('add',AddDevice.as_view(), name = "add-device"),
]
app_name = 'QoSAPI'