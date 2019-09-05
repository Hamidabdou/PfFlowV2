import json
from threading import Thread

from DynamicQoS.settings import MEDIA_ROOT
import requests
from datetime import date
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import *
from .models import *
from QoSmonitor.models import *


# Create your views here.
def index(request):
    topo = Topology.objects.create(topology_name="test2", topology_desc="test2")
    man = Access.objects.create(management_address="172.16.1.2", username="yassine", password="15")
    device = Device.objects.create(hostname="router1", topology_ref=topo, management=man)
    int1 = Interface.objects.create(interface_name="g0/0", device_ref=device, ingress=True)
    int2 = Interface.objects.create(interface_name="g0/1", device_ref=device, egress=True)
    # print(device.discovery_application())
    # ################################################################################"
    # url = "http://127.0.0.1:8000/api/v1/topology"
    # r = requests.get(url)
    # # # #
    # topologies = (r.json())
    # for topo in topologies['topologies']:
    #     top = Topology.objects.create(topology_name=topo['topology_name'], topology_desc=topo['topology_desc'])
    #     url = "http://127.0.0.1:8000/api/v1/topology?name=" + topo['topology_name']
    #     r = requests.get(url)
    #     devices = (r.json())
    #     for device in devices['devices']:
    #         man = device['management']
    #         mana = Access.objects.create(management_interface=man['management_interface'],
    #                                      management_address=man['management_address'],
    #                                      username=man['username'],
    #                                      password=man['password'])
    #         dev = Device.objects.create(hostname=device['hostname'], topology_ref=top, management=mana)
    #
    #         interfaces = device['interfaces']
    #         for interface in interfaces:
    #             if interface['interface_name'] != "Loopback0":
    #                 Interface.objects.create(device_ref=dev,
    #                                          interface_name=interface['interface_name'],
    #                                          egress=True)
    #     devices = Device.objects.filter(topology_ref=top)
    #     for device in devices:
    #         connection = device.connect()
    #         interfaces = connection.get_interfaces()
    #         for interface in interfaces:
    #             print(interface)
    #             print(interfaces[interface]['description'])
    #             if interfaces[interface]['description'] == "#ingress":
    #                 inter = Interface.objects.filter(device_ref=device, interface_name=interface)
    #                 if len(inter) != 0:
    #                     i = Interface.objects.get(device_ref=device, interface_name=interface)
    #                     i.ingress = True
    #                     i.egress = False
    #                     i.save()
    #                 else:
    #                     Interface.objects.create(device_ref=device,
    #                                              interface_name=interface,
    #                                              ingress=True)
    #             if interfaces[interface]['description'] == "#wan":
    #                 inter = Interface.objects.filter(device_ref=device, interface_name=interface)
    #                 if len(inter) != 0:
    #                     i = Interface.objects.get(device_ref=device, interface_name=interface)
    #                     i.wan = True
    #                     i.egress = False
    #                     i.save()
    #                 else:
    #                     Interface.objects.create(device_ref=device,
    #                                              interface_name=interface,
    #                                              wan=True)
    #
    #         connection.close()
    #         print('tttt')

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
    BusinessType.objects.create(name="protocol")
    with open(str(MEDIA_ROOT[0]) + "/monitoring_conf/nbar_application.json", 'r') as jsonfile:
        ap = json.load(jsonfile)
        for app in ap['applications']:
            BusinessApp(delay_ref=app['delay_ref'], loss_ref=app['loss_ref'], name=app['name'], match=app['match'],
                        recommended_dscp=app['recommended_dscp'],
                        business_type=BusinessType.objects.get(name=app['business_type'])).save()

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
    mark = request.POST['mark']
    begin = request.POST['begin_time']
    end = request.POST['end_time']
    source = request.POST['source']
    destination = request.POST['destination']
    if begin == '':
        begin = "00:00"
    if end == '':
        end = "23:59"
    if source == '':
        source = "any"
    if destination == '':
        destination = "any"
    if mark == '':
        mark = BusinessApp.objects.get(id=app_id).recommended_dscp

    # groupe = Group.objects.get(priority=request.POST['mark'], policy_id=police_id)

    app = Application(policy_in_id=PolicyIn.objects.get(policy_ref_id=police_id).id,
                      mark=mark,
                      business_type=BusinessType.objects.get(id=type_id),
                      business_app=BusinessApp.objects.get(id=app_id),
                      source=source,
                      destination=destination,
                      begin_time=begin,
                      end_time=end, )
    # dscp=Dscp.objects.get(dscp_value=app.mark,)
    if app.mark.startswith("A"):
        app.group = Group.objects.get(priority=app.app_priority, policy_id=police_id)
        app.save()
    if app.mark == "EF":
        app.group = Group.objects.get(priority="EF", policy_id=police_id)
        app.save()
    elif app.mark == "DEFAULT":
        app.group = Group.objects.get(priority="DEFAULT", policy_id=police_id)
        app.save()
    elif app.mark.startswith("C"):
        app.group = Group.objects.get(priority="SELECTOR", policy_id=police_id)
        app.save()
    else:
        app.save()

    return redirect('applications', police_id=police_id)


def add_custom_application(request, police_id):
    # app_form = AddApplicationForm(request.POST)
    # groupe = Group.objects.get(priority=request.POST['app_priority'], policy_id=police_id)

    app = Application(policy_in_id=PolicyIn.objects.get(policy_ref_id=police_id).id,
                      mark=request.POST['mark'],
                      source=request.POST['source'],
                      destination=request.POST['destination'],
                      begin_time=request.POST['begin_time'],
                      end_time=request.POST['end_time'],
                      protocol_type=request.POST['protocol_type'],
                      port_number=request.POST['port_number'],
                      custom_name=request.POST['custom_name'], )
    if app.mark.startswith("A"):
        app.group = Group.objects.get(priority=app.app_priority, policy_id=police_id)
        app.save()
    if app.mark == "EF":
        app.group = Group.objects.get(priority="EF", policy_id=police_id)
        app.save()
    elif app.mark == "DEFAULT":
        app.group = Group.objects.get(priority="DEFAULT", policy_id=police_id)
        app.save()
    elif app.mark.startswith("C"):
        app.group = Group.objects.get(priority="SELECTOR", policy_id=police_id)
        app.save()
    else:
        app.save()
    return redirect('applications', police_id=police_id)


def applications(request, police_id):
    police_in = PolicyIn.objects.get(policy_ref_id=police_id)
    apps = Application.objects.filter(policy_in=police_in)
    app_form = AddApplicationForm(request.POST)
    custom_form = AddCustomApplicationForm(request.POST)
    ctx = {'app_form': app_form, 'police_id': police_id, 'apps': apps, 'custom_form': custom_form}
    return render(request, 'devices2.html', context=ctx)


def policy_on(request, police_id):
    objs = Policy.objects.filter(enable=True)
    for k in objs:
        k.enable = False
        k.save()
    obj = Policy.objects.get(id=police_id)
    obj.enable = True
    obj.save()
    # return redirect('policies')
    return HttpResponseRedirect(reverse('policies', kwargs={}))


def policy_delete(request, policy_id):
    obj = Policy.objects.get(id=policy_id)
    obj.delete()
    return HttpResponseRedirect(reverse('policies', kwargs={}))


def policy_off(request, police_id):
    obj = Policy.objects.get(id=police_id)
    obj.enable = False
    obj.save()
    return HttpResponseRedirect(reverse('policies', kwargs={}))


@login_required(login_url='/login/')
def policies(request):
    policies = Policy.objects.all()

    if request.method == 'POST':
        policy_form = AddPolicyForm(request.POST)
        error = ''
        if policy_form.is_valid():
            a = policy_form.save()
            error = ''
            topo = request.POST['topologies']
            print(topo)
            devices = Device.objects.filter(topology_ref_id=topo)
            for device in devices:
                device.policy_ref = a
                device.save()
            police_id = a.id
            PolicyIn.objects.create(policy_ref=a)
            interfaces = Interface.objects.filter(ingress=False)
            # print(interfaces)
            Group.objects.create(name="real-time", priority="EF", policy=a)
            Group.objects.create(name="business", priority="4", policy=a)
            Group.objects.create(name="critical", priority="3", policy=a)
            Group.objects.create(name="non-business", priority="2", policy=a)
            Group.objects.create(name="non-business2", priority="1", policy=a)
            Group.objects.create(name="DEFAULT", priority="DEFAULT", policy=a)
            Group.objects.create(name="SELECTOR", priority="SELECTOR", policy=a)

            for interface in interfaces:
                po = PolicyOut.objects.create(policy_ref=a)
                interface.policy_out_ref = po
                interface.save()
                # print(interface)

                realtime = RegroupementClass.objects.create(priority="100",
                                                            group=Group.objects.get(priority="EF", policy=a),
                                                            policy_out=po)
                Dscp.objects.create(dscp_value="EF", regroupement_class=realtime)
                policing = Policing.objects.create(cir="10", pir="10", dscp_transmit="AF31")
                shaping = Shaping.objects.create(peak="10", average="10")
                high = RegroupementClass.objects.create(shaping=shaping, policing=policing, bandwidth="10",
                                                        group=Group.objects.get(priority="4", policy=a),
                                                        policy_out=po)
                Dscp.objects.create(dscp_value="AF43", regroupement_class=high, drop_max="10", drop_min="5",
                                    denominator="8")
                Dscp.objects.create(dscp_value="AF42", regroupement_class=high, drop_max="10", drop_min="5",
                                    denominator="8")
                Dscp.objects.create(dscp_value="AF41", regroupement_class=high, drop_max="10", drop_min="5",
                                    denominator="8")
                policing = Policing.objects.create(cir="10", pir="10", dscp_transmit="AF31")
                shaping = Shaping.objects.create(peak="10", average="10")
                priority = RegroupementClass.objects.create(shaping=shaping, policing=policing, bandwidth="10",
                                                            group=Group.objects.get(priority="3", policy=a),
                                                            policy_out=po)
                Dscp.objects.create(dscp_value="AF33", regroupement_class=priority, drop_max="10", drop_min="5",
                                    denominator="8")
                Dscp.objects.create(dscp_value="AF32", regroupement_class=priority, drop_max="10", drop_min="5",
                                    denominator="8")
                Dscp.objects.create(dscp_value="AF31", regroupement_class=priority, drop_max="10", drop_min="5",
                                    denominator="8")
                policing = Policing.objects.create(cir="10", pir="10", dscp_transmit="AF31")
                shaping = Shaping.objects.create(peak="10", average="10")
                med = RegroupementClass.objects.create(shaping=shaping, policing=policing, bandwidth="10",
                                                       group=Group.objects.get(priority="2", policy=a),
                                                       policy_out=po)
                Dscp.objects.create(dscp_value="AF23", regroupement_class=med, drop_max="10", drop_min="5",
                                    denominator="8")
                Dscp.objects.create(dscp_value="AF22", regroupement_class=med, drop_max="10", drop_min="5",
                                    denominator="8")
                Dscp.objects.create(dscp_value="AF21", regroupement_class=med, drop_max="10", drop_min="5",
                                    denominator="8")
                policing = Policing.objects.create(cir="10", pir="10", dscp_transmit="AF31")
                shaping = Shaping.objects.create(peak="10", average="10")
                low = RegroupementClass.objects.create(shaping=shaping, policing=policing, bandwidth="10",
                                                       group=Group.objects.get(priority="1", policy=a),
                                                       policy_out=po)
                Dscp.objects.create(dscp_value="AF13", regroupement_class=low, drop_max="10", drop_min="5",
                                    denominator="8")
                Dscp.objects.create(dscp_value="AF12", regroupement_class=low, drop_max="10", drop_min="5",
                                    denominator="8")
                Dscp.objects.create(dscp_value="AF11", regroupement_class=low, drop_max="10", drop_min="5",
                                    denominator="8")

            return redirect('policies')
        else:
            error = 'name error'

        return render(request, 'policy.html', locals())
    else:
        # print(RegroupementClass.objects.all())
        policy_form = AddPolicyForm(request.POST)
        return render(request, 'policy.html', locals())


@login_required(login_url='/login/')
def policy_deployment(request, police_id):
    # policeIn = PolicyIn.objects.get(policy_ref_id=police_id)
    devices = Device.objects.filter(policy_ref_id=police_id)
    threads = []
    for device in devices:
        threads.append(Thread(target=device.deploy_policy, args=police_id))
    for th in threads:
        print("start thread")
        th.start()
    for th in threads:
        th.join()
    policy = Policy.objects.get(id=police_id)
    policy.deploy = True
    policy.save()
    # apps = Application.objects.filter(policy_in=policeIn)
    # for device in devices:
    #     if device.wan() or device.ingress():
    #         connection = device.connect()
    #         for app in apps:
    #             time_config = app.render_time_range
    #             connection.load_merge_candidate(config=time_config)
    #             connection.commit_config()
    #             app_config = app.acl_list
    #             connection.load_merge_candidate(config=app_config)
    #             connection.commit_config()
    #         config_file = policeIn.render_policy
    #         connection.load_merge_candidate(config=config_file)
    #         connection.commit_config()
    #         connection.close()
    # policiesOUt = PolicyOut.objects.filter(policy_ref_id=police_id)
    # for device in devices:
    #     if device.egress():
    #         connection = device.connect()
    #         for policy in policiesOUt:
    #             config_file = policy.render_policy
    #             connection.load_merge_candidate(config=config_file)
    #             connection.commit_config()
    #         connection.close()
    # for device in devices:
    #     device.deploy_policy(police_id)
    # connection = device.connect()
    # config_file = device.service_policy()
    # connection.load_merge_candidate(config=config_file)
    # connection.commit_config()
    # connection.close()

    # dscps = Dscp.objects.all()
    # for d in dscps:
    #     print(d.dscp_value+":" + str(d.delay_ref))
    #     print(d.dscp_value + ":" + str(d.delay))
    #     print("delay ratio" + ":" + str(d.delay_ratio))
    #     print("loss ratio" + ":" + str(d.loss_ratio))
    #     print(d.dscp_value + ":" + str(d.c_ratio))
    #     print(d.dscp_value + ":" + str(d.ratio))

    # for po in policiesOUt:
    #     interface = Interface.objects.get(policy_out_ref=po)
    #     print(interface.tuning())
    #     regs = RegroupementClass.objects.filter(policy_out=po)
    #     for reg in regs:
    #         if reg.priority == "100":
    #             print('ef')
    #         else:
    #             print("------------------")
    #             print("test commit")
    #             if reg.oppressed_tos is not None:
    #                 print(reg.oppressed_tos.dscp_value)
    #             if reg.excessive_tos is not None:
    #                 print(reg.excessive_tos.dscp_value)

    # for app in apps:
    #     print(app.render_time_range)
    #     print(app.acl_list)
    # h= Dscp.objects.all()
    # for i in h:
    #     print(i.delay_ref)

    # for device in devices:
    #     print(device.no_service_policy())
    # print(policeIn.render_no_policy)
    # for app in apps:
    #     # print(app.render_time_range)
    #     print(app.render_no_acl)
    # for p in policiesOUt:
    #     print(p.render_no_policy)
    #     print(p.render_policy)
    # # print(police)
    # config_file = police.render_policy
    # apps = Application.objects.filter(policy_in=police)
    # topo = Topology.objects.create(topology_name="test2", topology_desc="test2")
    # man = Access.objects.create(management_address="172.16.1.2", username="yassine", password="15")
    # device = Device.objects.create(hostname="router1", topology_ref=topo, management=man)
    # int1 = Interface.objects.create(interface_name="g0/0", device_ref=device, ingress=True)
    # int2 = Interface.objects.create(interface_name="g0/1", device_ref=device, ingress=False)
    # device = Device.objects.get(id=1)
    # po = PolicyOut.objects.filter(policy_ref_id=police_id)
    # connection = device.connect()
    # print(connection.get_environment())
    # for p in po:
    # connection.load_merge_candidate(config=p.render_policy)
    # connection.commit_config()

    # print(config_file)
    #
    # # # for app in apps:
    # print(connection.load_merge_candidate(config=config_file))
    #
    # connection.commit_config()
    #
    # connection.close()

    # print(config_file)

    # driver = get_network_driver("ios")
    # router = Device.objects.get(id=1)
    # device = driver(router.management.management_address, router.management.username,
    #                 router.management.password)
    # try:
    #     device.open()
    #     device.load_merge_candidate(config=config_file)
    #     device.commit_config()
    #     device.close()
    # except Exception as e:
    #     print(e)

    return HttpResponseRedirect(reverse('devices', kwargs={'policy_id': police_id}))


def devices(request, policy_id):
    devices = Device.objects.filter(policy_ref_id=policy_id)
    device_len = len(devices)
    wan = 0
    ingress = 0
    egress = 0
    for device in devices:
        interfaces = Interface.objects.filter(device_ref=device)
        for interface in interfaces:
            if interface.wan:
                wan = wan + 1
            if interface.ingress:
                ingress = ingress + 1
            if interface.egress:
                egress = egress + 1
    applications = Application.objects.filter(policy_in=PolicyIn.objects.get(policy_ref_id=policy_id))
    applications_len = len(applications)
    today = date.today()
    groups = Group.objects.filter(policy_id=policy_id)
    for group in groups:
        print(group.all_applications)
    policy = Policy.objects.get(id=policy_id)

    return render(request, 'devices_template.html', locals())


def nbar_discover(request, policy_id):
    devices = Device.objects.filter(policy_ref_id=policy_id)
    threads = []
    for device in devices:
        threads.append(Thread(target=device.enable_nbar))
    for th in threads:
        print("start thread")
        th.start()
    for th in threads:
        th.join()
    return HttpResponse("nbar activated")


@login_required(login_url='/login/')
def nbar_discover_applications(request, policy_id):
    devices = Device.objects.filter(policy_ref_id=policy_id)
    application = []
    nbar_apps = Application.objects.all()
    apps = BusinessApp.objects.all()
    for device in devices:
        application.extend(device.discovery_application())
    for app in set(application):
        c = False
        b = BusinessApp.objects.filter(name=app)
        for a in b:
            b_id = a.id
            if len(Application.objects.filter(business_app=a, policy_in=PolicyIn.objects.get(policy_ref=policy_id))):
                c = True
        # c =
        if len(b) != 0 and not c:
            ap = Application.objects.create(business_app=BusinessApp.objects.get(id=b_id),
                                            business_type=BusinessApp.objects.get(id=b_id).business_type,
                                            policy_in=PolicyIn.objects.get(policy_ref_id=policy_id),
                                            mark=BusinessApp.objects.get(id=b_id).recommended_dscp)
            if ap.mark.startswith("A"):
                ap.group = Group.objects.get(priority=app.app_priority, policy_id=policy_id)
                ap.save()
            elif ap.mark == "EF":
                ap.group = Group.objects.get(priority="EF", policy_id=policy_id)
                ap.save()
            elif ap.mark == "DEFAULT":
                ap.group = Group.objects.get(priority="DEFAULT", policy_id=policy_id)
                ap.save()
            else:
                ap.save()

    return HttpResponse("discover done!!!!")


@login_required(login_url='/login/')
def policy_remove(request, police_id):
    devices = Device.objects.filter(policy_ref_id=police_id)
    threads = []
    for device in devices:
        threads.append(Thread(target=device.remove_policy, args=police_id))
    for th in threads:
        print("start thread")
        th.start()
    for th in threads:
        th.join()
    policy = Policy.objects.get(id=police_id)
    policy.deploy = False
    policy.save()
    return HttpResponseRedirect(reverse('devices', kwargs={'policy_id': police_id}))


def load_applications(request):
    business_type_id = request.GET.get('business_type')
    business_apps = BusinessApp.objects.filter(business_type_id=business_type_id).order_by('name')
    return render(request, 'application_dropdown_list_options.html', {'business_apps': business_apps})


def policy_dashboard(request, policy_id):
    return render(request, 'policy_dashbord.html', locals())


def tuning(request, policy_id):
    return render(request, 'tuning.html', locals())
