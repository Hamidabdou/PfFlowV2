import json

import requests
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import *
from .models import *


# Create your views here.
def index(request):
    #
    # topo = Topology.objects.create(topology_name="test", topology_desc="test")
    # device = Device.objects.create(hostname="router1", topology_ref=topo)
    # int1 = Interface.objects.create(interface_name="g0/0", device_ref=device, ingress=True)
    # int2 = Interface.objects.create(interface_name="g1/0", device_ref=device, ingress=True)
    # int3 = Interface.objects.create(interface_name="g2/0", device_ref=device, ingress=False)
    # int4 = Interface.objects.create(interface_name="g3/0", device_ref=device, ingress=False)
    # #
    # # url = "http://192.168.0.128:8080/qosapi/topologies"
    # # r = requests.get(url)
    # #
    # # topo = (r.json())
    # # # print(type(topo))
    # # print(topo['topologies'])
    # # for topolo in topo['topologies']:
    # #     top = Topology.objects.create(topology_name=topolo['topology_name'], topology_desc=topolo['topology_desc'])
    # #     devices = topolo['devices']
    # #     for device in devices:
    # #         man = device['management']
    # #         mana = Access.objects.create(management_interface=man['management_interface'],
    # #                                      management_address=['management_address'],
    # #                                      username=['username'],
    # #                                      password=['password'])
    # #         dev = Device.objects.create(hostname=device['hostname'], topology_ref=top,management=mana)
    # #         interfaces = device['interfaces']
    # #         for interface in interfaces:
    # #             Interface.objects.create(device_ref=dev,
    # #                                      interface_name=interface['interface_name'],
    # #                                      ingress=interface['ingress'])
    # #
    # # interfaces=Interface.objects.all()
    # # for i in interfaces:
    # #     print(i.device_ref)
    #
    #     #print(devices)
    # # for device in topo['topologies']:
    # #     Device.objects.create(hostname=device['hostname'])
    #
    # # json_url = urlopen(url)
    # #
    # # data = json.loads(json_url)
    # #
    # # print(data)
    BusinessType.objects.create(name="Application")
    BusinessType.objects.create(name="application-group")
    BusinessType.objects.create(name="Category")
    BusinessType.objects.create(name="sub-category")
    BusinessType.objects.create(name="device-class")
    BusinessType.objects.create(name="media-type")
    ss='application-group'
    print(BusinessType.objects.get(name=ss))
    with open("/home/djoudi/PycharmProjects/PfFlowV2/DynamicQoS/QoSmanager/nbar_application.json", 'r') as jsonfile:
        ap = json.load(jsonfile)
        for app in ap['applications']:
            s = app['business_type']
            BusinessApp(name=app['name'], match=app['match'],
                        business_type=BusinessType.objects.get(name=str(s))).save()
    # police = PolicyIn.objects.get(id=1)
    #
    # apps = Application.objects.filter(policy_in=police)
    # print(apps)
    # for ap in apps:
    #     print(ap.render_time_range)
    #
    # print(police.name)
    # print(police.render_policy)
    # device=Device.objects.all()
    # for d in device:
    #     print(d.service_policy())
    # out=PolicyOut.objects.all()
    # for o in out:
    #     print(o.render_policy)

    # return render(request, 'home.html')
    return HttpResponse("hello")


def add_application(request, police_id):
    # app_form = AddApplicationForm(request.POST)
    app_id = request.POST['business_app']
    type_id = request.POST['business_type']
    groupe = Group.objects.get(priority=request.POST['app_priority'], policy_id=police_id)

    Application(policy_in_id=PolicyIn.objects.get(policy_ref_id=police_id).id,
                drop_prob=request.POST['drop_prob'],
                app_priority=request.POST['app_priority'],
                business_type=BusinessType.objects.get(id=type_id),
                business_app=BusinessApp.objects.get(id=app_id),
                group=groupe,
                source=request.POST['source'],
                destination=request.POST['destination'],
                begin_time=request.POST['begin_time'],
                end_time=request.POST['end_time'], ).save()
    return redirect('applications', police_id=police_id)


def add_custom_application(request, police_id):
    # app_form = AddApplicationForm(request.POST)
    groupe = Group.objects.get(priority=request.POST['app_priority'], policy_id=police_id)

    Application(policy_in_id=PolicyIn.objects.get(policy_ref_id=police_id).id,
                drop_prob=request.POST['drop_prob'],
                app_priority=request.POST['app_priority'],
                group=groupe,
                source=request.POST['source'],
                destination=request.POST['destination'],
                begin_time=request.POST['begin_time'],
                end_time=request.POST['end_time'],
                protocol_type=request.POST['protocol_type'],
                port_number=request.POST['port_number'],
                custom_name=request.POST['custom_name'], ).save()
    return redirect('applications', police_id=police_id)


def applications(request, police_id):
    police_in = PolicyIn.objects.get(policy_ref_id=police_id)
    apps = Application.objects.filter(policy_in=police_in)
    app_form = AddApplicationForm(request.POST)
    custom_form = AddCustomApplicationForm(request.POST)
    ctx = {'app_form': app_form, 'police_id': police_id, 'apps': apps, 'custom_form': custom_form}
    return render(request, 'devices.html', context=ctx)


# def add_policy(request):
#     policy_form = AddPolicyForm(request.POST or None)
#     error = ''
#     if policy_form.is_valid():
#         a = policy_form.save()
#
#         # a = Policy(name=request.POST['name'], description=request.POST['description'])
#
#         # a.save()
#         devices = Device.objects.all()
#         for device in devices:
#             device.policy_ref = a
#             device.save()
#         police_id = a.id
#         PolicyIn.objects.create(policy_ref=a)
#         interfaces = Interface.objects.filter(ingress=False)
#         Group.objects.create(name="business", priority="4", policy=a)
#         Group.objects.create(name="critical", priority="3", policy=a)
#         Group.objects.create(name="non-business", priority="2", policy=a)
#         Group.objects.create(name="non-business2", priority="1", policy=a)
#         for interface in interfaces:
#             po = PolicyOut.objects.create(policy_ref=a)
#             interface.policy_out_ref = po
#             interface.save()
#             RegroupementClass.objects.create(group=Group.objects.get(priority="4", policy=a),
#                                              policy_out=po)
#             RegroupementClass.objects.create(group=Group.objects.get(priority="3", policy=a),
#                                              policy_out=po)
#             RegroupementClass.objects.create(group=Group.objects.get(priority="2", policy=a),
#                                              policy_out=po)
#             RegroupementClass.objects.create(group=Group.objects.get(priority="1", policy=a),
#                                              policy_out=po)
#         else:
#             error = 'field error'
#     # BusinessType.objects.create(name="Application")
#     # BusinessType.objects.create(name="application-group")
#     # BusinessType.objects.create(name="Category")
#     # BusinessType.objects.create(name="sub-category")
#     # BusinessType.objects.create(name="device-class")
#     # BusinessType.objects.create(name="media-type")
#     # with open("/home/djoudi/PycharmProjects/DynamicQoS/DynamicQoS/QoSmanager/nbar_application.json", 'r') as jsonfile:
#     #     ap = json.load(jsonfile)
#     #     for app in ap['applications']:
#     #         bu = BusinessType.objects.get(name=app['business_type'])
#     #         BusinessApp(name=app['name'], match=app['match'], business_type=bu).save()
#
#     return redirect('policies')


def delete_policy(request, police_id):
    obj = Policy.objects.get(id=police_id)
    obj.delete()
    return redirect('policies')


def policy_on(request, police_id):
    obj = Policy.objects.get(id=police_id)
    obj.enable = True
    obj.save()
    objs = Policy.objects.filter(~Q(id=police_id))
    for k in objs:
        k.enable = False
        k.save()
    # return redirect('policies')
    return HttpResponse("test")


def policy_off(request, police_id):
    obj = Policy.objects.get(id=police_id)
    obj.enable = False
    obj.save()
    return HttpResponse("off")


def policies(request):
    policies = Policy.objects.all()

    if request.method == 'POST':
        policy_form = AddPolicyForm(request.POST)
        error = ''
        if policy_form.is_valid():
            a = policy_form.save()
            error = ''
            devices = Device.objects.all()
            for device in devices:
                device.policy_ref = a
                device.save()
            police_id = a.id
            PolicyIn.objects.create(policy_ref=a)
            interfaces = Interface.objects.filter(ingress=False)
            Group.objects.create(name="business", priority="4", policy=a)
            Group.objects.create(name="critical", priority="3", policy=a)
            Group.objects.create(name="non-business", priority="2", policy=a)
            Group.objects.create(name="non-business2", priority="1", policy=a)
            for interface in interfaces:
                po = PolicyOut.objects.create(policy_ref=a)
                interface.policy_out_ref = po
                interface.save()
                RegroupementClass.objects.create(group=Group.objects.get(priority="4", policy=a),
                                                 policy_out=po)
                RegroupementClass.objects.create(group=Group.objects.get(priority="3", policy=a),
                                                 policy_out=po)
                RegroupementClass.objects.create(group=Group.objects.get(priority="2", policy=a),
                                                 policy_out=po)
                RegroupementClass.objects.create(group=Group.objects.get(priority="1", policy=a),
                                                 policy_out=po)

            return redirect('policies')
        else:
            error = 'name error'

        return render(request, 'policy.html', locals())
    else:
        policy_form = AddPolicyForm(request.POST)
        return render(request, 'policy.html', locals())


def load_applications(request):
    business_type_id = request.GET.get('business_type')
    business_apps = BusinessApp.objects.filter(business_type_id=business_type_id).order_by('name')
    return render(request, 'application_dropdown_list_options.html', {'business_apps': business_apps})


# Create your views here.
