from QoSmanager import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('ajax/load-applications/', views.load_applications, name='ajax_load_applications'),
    path('applications/<police_id>', views.applications, name='applications'),
    path('add_application/<police_id>', views.add_application, name='add_application'),
    path('add_custom_application/<police_id>', views.add_custom_application, name='add_custom_application'),
    path('policies/', views.policies, name='policies'),
    # path('add_policy/', views.add_policy, name='add_policy'),
    path('delete_policy/<police_id>', views.delete_policy, name='delete_policy'),
    path('policy_on/<police_id>', views.policy_on, name='policy_on'),
    path('policy_off/<police_id>', views.policy_off, name='policy_off'),
    path('policy_deployment/<police_id>', views.policy_deployment, name='policy_deployment'),
    path('policy_remove/<police_id>', views.policy_remove, name='policy_remove'),
    path('devices/<topology_id>', views.devices, name='devices'),
    path('nbar_discover/<topology_id>', views.nbar_discover, name='nbar_discover'),
    path('nbar_discover_applications/<topology_id>', views.nbar_discover_applications, name='nbar_discover_applications'),

]
