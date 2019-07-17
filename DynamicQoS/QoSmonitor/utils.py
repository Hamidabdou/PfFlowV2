import hashlib 
import mongoengine
from scapy.all import * 
from scapy.layers.netflow import NetflowSession
from functools import partial
from .models import * 
from ntplib import * 


def dbcollect(phb_behavior:topology,pkt):
        sys_uptime = pkt[NetflowHeaderV9].sysUptime
        devices = phb_behavior.devices
        monitor = None 
        for device in devices:
            if (device.management.management_address == pkt[IP].src):
                    monitor = device
        flows = None
        try:
                flows = pkt[NetflowDataflowsetV9].records
                for record in flows:
                    netflow_fields_ins = netflow_fields()
                    netflow_fields_ins.counter_bytes = int.from_bytes(record.IN_BYTES,'big')
                    netflow_fields_ins.counter_pkts = int.from_bytes(record.IN_PKTS,'big')
                    netflow_fields_ins.first_switched = datetime.datetime.fromtimestamp(record.FIRST_SWITCHED)
                    netflow_fields_ins.last_switched = datetime.datetime.fromtimestamp(record.LAST_SWITCHED)
                    netflow_fields_ins.bandwidth = int.from_bytes(record.IN_BYTES,'big') * 8 / (record.LAST_SWITCHED - record.FIRST_SWITCHED) / 100 #bps 
                    input_interface = monitor.get_interface_by_index(int.from_bytes(record.INPUT_SNMP,'big'))
                    netflow_fields_ins.input_int = input_interface
                    output_interface = monitor.get_interface_by_index(int.from_bytes(record.OUTPUT_SNMP,'big'))
                    netflow_fields_ins.output_int = output_interface
                    netflow_fields_ins.collection_time = datetime.datetime.fromtimestamp(sys_uptime)
                    flow_input = "{}:{}->{}:{}|{}|{}|{}".format(str(record.IPV4_SRC_ADDR),str(record.L4_SRC_PORT),str(record.IPV4_DST_ADDR) , str(record.L4_SRC_PORT) ,str(record.TOS) , str(int.from_bytes(record.APPLICATION_ID,'big')),str(record.PROTOCOL))
                    flow_hash = hashlib.md5(flow_input.encode())
                    src_device , dst_device = phb_behavior.get_ip_sla_devices(record)
                    flow_exist = None
                    flow_exist = flow.objects(flow_id= flow_hash.hexdigest())
                    if not(flow_exist):
                            flow_ins = flow() 
                            flow_ins.flow_id = str(flow_hash.hexdigest())
                            flow_ins.ipv4_src_addr = record.IPV4_SRC_ADDR
                            flow_ins.ipv4_dst_addr = record.IPV4_DST_ADDR
                            flow_ins.ipv4_protocol = record.PROTOCOL
                            flow_ins.transport_src_port = record.L4_SRC_PORT
                            flow_ins.transport_dst_port = record.L4_DST_PORT
                            flow_ins.type_of_service = record.TOS
                            flow_ins.application_ID = int.from_bytes(record.APPLICATION_ID,'big')
                            flow_ins.save()
                            netflow_fields_ins.flow_ref = flow_ins
                            netflow_fields_ins.device = monitor
                            netflow_fields_ins.save()
                            if (src_device != dst_device):
                                similar_ip_sla = ip_sla.objects(sender_device_ref = src_device , responder_device_ref = dst_device, type_of_service = record.TOS) #verify if ip sla exists for this flow 
                                if (len(similar_ip_sla) == 0 ):
                                    dst_device.configure_ip_sla_responder()
                                    sla = ip_sla()
                                    sla.sender_device_ref = src_device
                                    sla.responder_device_ref = dst_device
                                    sla.type_of_service = record.TOS 
                                    sla.save()
                                    src_device.configure_ip_sla(sla.operation,record,dst_device)
                                    flow_ins.ip_sla_ref = sla 
                                else:
                                    flow_ins.ip_sla = similar_ip_sla
                                    print(similar_ip_sla[0].operation)
                                    jitter, delay = src_device.pull_ip_sla_stats(similar_ip_sla[0].operation)
                                    sla_info_ins = ip_sla_info()
                                    sla_info_ins.avg_jitter = jitter 
                                    sla_info_ins.avg_delay = delay 
                                    sla_info_ins.timestamp = datetime.datetime.fromtimestamp(sys_uptime)
                                    sla_info_ins.ip_sla_ref = similar_ip_sla[0]
                                    sla_info_ins.save()

                    else:
                            netflow_fields_ins.device = monitor
                            netflow_fields_ins.flow_ref = flow_exist[0]
                            netflow_fields_ins.save()
                            sla = ip_sla.objects(sender_device_ref = src_device , responder_device_ref = dst_device, type_of_service = flow_exist[0].type_of_service)
                            jitter , delay = src_device.pull_ip_sla_stats(sla[0].operation)
                            sla_info = ip_sla_info()
                            sla_info.avg_jitter = jitter 
                            sla_info.avg_delay = delay
                            sla_info.timestamp = datetime.datetime.fromtimestamp(sys_uptime)
                            sla_info.ip_sla_ref = sla
                            sla_info.save() 
        except Exception:
            try:
                app_name = pkt[NetflowDataflowsetV9][NetflowOptionsRecordOptionV9].APPLICATION_NAME
                app_id = pkt[NetflowDataflowsetV9][NetflowOptionsRecordOptionV9].APPLICATION_ID
                app_ins = application(application_ID = app_id,application_NAME = app_name)
                app_ins.save()
            except Exception:
                print("Unknown packet")



def Sniff_Netflow(phb_behavior):
        sniff(session = NetflowSession , filter = "dst port 2055", prn = partial(dbcollect,phb_behavior))


def valid_cover(graph, cover):
    valid = True
    num_edge = [0] * len(graph)
    for i in range(0, len(graph)):
        for j in range(i, len(graph)):
            if graph[i][j] == 1:
                if (i not in cover) and (j not in cover):
                    valid = False
                    num_edge[i] += 1
                    num_edge[j] += 1
    return valid, num_edge

def check_if_exists(cls, *args, **kwargs):
    try:
        ob = cls.objects.get(*args, **kwargs)
        return True
    except cls.DoesNotExist:
        return False