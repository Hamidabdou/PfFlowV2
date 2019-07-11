from django.urls import path 

from .views import AddDevice, MyOwnView

urlpatterns = [
    path('add',AddDevice.as_view(), name = "add-device"),
    path('topologies',MyOwnView.as_view(), name = "topologies"),
]
app_name = 'QoSAPI'