import hashlib 
from mongoengine import *
import mongoengine
from mongoengine import * 
from scapy.all import * 
from scapy.layers.netflow import NetflowSession
from functools import partial
from models import * 


def dbcollect(phb_behavior:topology,pkt):


        sys_uptime = pkt[NetflowHeaderV9].sysUptime
        devices = phb_behavior.devices
        monitor = None 
        for device in devices:
                if (device.loopback_addr == pkt[IP].src):
                        monitor = device
        flows = None
        try:
                flows = pkt[NetflowDataflowsetV9].records
        except Exception as e :
                print(e)
        try:
                for record in flows:

                        # fill the fields of netflow in each monitor
                        netflow_fields_ins = netflow_fields()
                        netflow_fields_ins.counter_bytes = int.from_bytes(record.IN_BYTES,'big')
                        netflow_fields_ins.counter_pkts = int.from_bytes(record.IN_PKTS,'big')
                        netflow_fields_ins.first_switched = record.FIRST_SWITCHED
                        netflow_fields_ins.last_switched = record.LAST_SWITCHED
                        netflow_fields_ins.input_int = int.from_bytes(record.INPUT_SNMP,'big')
                        netflow_fields_ins.output_int = int.from_bytes(record.OUTPUT_SNMP,'big')
                        netflow_fields_ins.collection_time = sys_uptime

                        #calculate the bandwidth in bps
                        #netflow_fields_ins.bandwidth = (record.LAST_SWITCHED - record.FIRST_SWITCHED) / 1000 * 8 * record.IN_PKTS  


                        # create the flow and verify if it exist
                        flow_input = "{}:{}->{}:{}|{}|{}|{}".format(str(record.IPV4_SRC_ADDR),str(record.L4_SRC_PORT),str(record.IPV4_DST_ADDR) , str(record.L4_SRC_PORT) ,str(record.TOS) , str(int.from_bytes(record.APPLICATION_ID,'big')),str(record.PROTOCOL))

                        flow_hash = hashlib.md5(flow_input.encode())
                        print("quering the database if flow exists")

                        src_device , dst_device = phb_behavior.get_ip_sla_devices(record)

                        flow_exist = None
                        flow_exist = flow.objects(flow_id= flow_hash.hexdigest())
                        print(flow_exist)
                        if not(flow_exist):
                                print("new flow is occured")
                                flow_ins = flow()
                                flow_ins.flow_id = str(flow_hash.hexdigest())
                                flow_ins.ipv4_src_addr = record.IPV4_SRC_ADDR
                                flow_ins.ipv4_dst_addr = record.IPV4_DST_ADDR
                                flow_ins.ipv4_protocol = record.PROTOCOL
                                flow_ins.transport_src_port = record.L4_SRC_PORT
                                flow_ins.transport_dst_port = record.L4_DST_PORT
                                flow_ins.type_of_service = record.TOS
                                flow_ins.application_name = int.from_bytes(record.APPLICATION_ID,'big')
                                flow_ins.save()
                                netflow_fields_ins.flow_ref = flow_ins
                                netflow_fields_ins.device = monitor
                                netflow_fields_ins.save()
                                print("new flow is added")
                                dst_device.configure_ip_sla_responder()
                                sla = ip_sla()
                                print("new ip sla is configured for this flow")
                                sla.device_ref = src_device
                                sla.flow_ref = flow_ins
                                sla.save()
                                src_device.configure_ip_sla(sla.operation,record) # TODO : be more specfic in the interface loopback of the dst_device
                        else:
                                netflow_fields_ins.device = monitor
                                netflow_fields_ins.flow_ref = flow_exist[0]
                                netflow_fields_ins.save()
                                
                                sla = ip_sla.objects(flow_ref = flow_exist[0] , device_ref = src_device )
                                jitter , delay = src_device.pull_ip_sla_stats(sla.operation)
                                sla_info = ip_sla_info()
                                sla_info.avg_jitter = jitter 
                                sla_info.avg_delay = delay 
                                sla_info.flow_ref = flow_exist[0]
                                sla_info.ip_sla_ref = sla
                                sla_info.save() 
        except Exception as e :
                print(e)


def Sniff_Netflow(phb_behavior):
        sniff(session = NetflowSession , filter = "dst port 2055", prn = partial(dbcollect,phb_behavior))



def dbconnect(dbname,username,password):
        mongoengine.connect(dbname,username,password)


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