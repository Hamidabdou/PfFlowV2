from django.urls import path
from django.contrib.auth import views as loginview
from QoSGui.forms import LoginForm
from . import views

urlpatterns = [
    path('login/', loginview.login, {'authentication_form': LoginForm}),
    path('', views.home, name='Home'),
    path('topologies/', views.topologies, name='Topologies'),
    path('addtopology/', views.add_topology, name='AddTopology'),
    path('drag_drop/<topo_id>', views.drag_drop, name='drag_drop'),
    path('saveTopology/<topo_id>', views.save_json_topology, name='SaveTopology'),
]

