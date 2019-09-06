from background_task import background
import requests

from .utils import *
from .models import *
from datetime import datetime
import time
import paho.mqtt.client as mqtt

server = "postman.cloudmqtt.com"
port = 11494
username = "qvjbfmpb"
password = "x6lBEK-EESRM"
my_client = mqtt.Client()


def connect():
    my_client.username_pw_set(username=username, password=password)
    my_client.connect(host=server, port=port)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # subscription in on_connect means that the subscription will be renewed
    # if we re-connect in case of loosing the connection
    # client.subscribe("$SYS/#")


def publish(topic, payload, qos, retain):
    return my_client.publish(topic=topic, payload=payload, qos=qos, retain=retain)


def on_publish(client, userdata, mid):
    print("mid: " + str(mid))


@background(queue='q1')
def sniff_back(phb_behavior):
    topo = topology.objects(topology_name=phb_behavior)[0]
    print("Strting ... ")
    Sniff_Netflow(topo)
    return None


@background(queue='q2')
def Initialize_mqtt_client():
    my_client.on_connect = on_connect
    my_client.on_publish = on_publish
    connect()
    time.sleep(5)
    publish(topic="LimitBreach/J", payload="Jitter Limit breach", qos=1, retain=False)

    slainfo = ip_sla_info.objects(avg_jitter__lte=5)

    for sla in slainfo:
        publish(topic="LimitBreach/J", payload="Jitter Limit breach", qos=1, retain=False)

    notification_ins = notification(message="Jitter Breach", timestampt=str(datetime.now()))

    my_client.loop_forever()
    return None


@background(queue='q1')
def add_device_api_call1(topology_name, management_interface, management_address, username, password):
    json_data = {"management": {"management_interface": management_interface, "management_address": management_address,
                                "username": username, "password": password}, "topology_name": topology_name}
    print(topology_name, management_address, management_interface, username, password)
    api_url = "http://localhost:8000/api/v1/add-device"
    response = requests.post(url=api_url, json=json_data)
    print(response.status_code)
    print(response.content)

    return response.content


def prepare_env_api_call(topology_name):
    json_data = {"topology": topology_name}
    print(topology_name)

    api_url = "http://localhost:8000/api/v1/preapare-env"
    response = requests.post(url=api_url, json=json_data)
    print(response.status_code)
    print(response.content)

    return response.content


def discover_network_api_call(topology_name):
    json_data = {"topology": topology_name}

    api_url = "http://localhost:8000/api/v1/discover-network"
    response = requests.post(url=api_url, json=json_data)
    print(response.status_code)
    print(response.content)

    return response.content


def configure_monitoring_api_call(topology_name, destination):
    json_data = {"topology": topology_name, "destination": destination}

    api_url = "http://localhost:8000/api/v1/configure-monitoring"
    response = requests.post(url=api_url, json=json_data)
    print(response.status_code)
    print(response.content)

    return response.content


def start_monitoring_api_call(topology_name):
    json_data = {"topology": topology_name}

    api_url = "http://localhost:8000/api/v1/start-monitoring"
    response = requests.post(url=api_url, json=json_data)
    print(response.status_code)
    print(response.content)

    return response.content


@background(schedule=60)
def nbar_discovery_task(end_time, id_policy):
    dvcs = Device.objects.filter(policy_ref_id=id_policy)
    threads = []
    for dvcs in dvcs:
        threads.append(Thread(target=dvcs.enable_nbar))
    for th in threads:
        print("start thread")
        th.start()
    for th in threads:
        th.join()

    while datetime.now() < datetime.strptime(end_time,'%Y/%m/%d %H:%M'):
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
                if len(Application.objects.filter(business_app=a,
                                                  policy_in=PolicyIn.objects.get(policy_ref=policy_id))):
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
        time.sleep(300)
