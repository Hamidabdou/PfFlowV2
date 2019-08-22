import napalm
from DynamicQoS.settings import MEDIA_ROOT
from django.db import models
# Create your models here.
from jinja2 import Environment, FileSystemLoader
from napalm import get_network_driver
from netaddr import *
from netmiko import ConnectHandler


class Topology(models.Model):
    topology_name = models.CharField(max_length=45)
    topology_desc = models.CharField(max_length=45)

    def __str__(self):
        return self.topology_name


class BusinessType(models.Model):
    name = models.CharField(max_length=45, unique=True)

    def __str__(self):
        return self.name


class BusinessApp(models.Model):
    name = models.CharField(max_length=45)
    business_type = models.ForeignKey(BusinessType, on_delete=models.CASCADE, null=True)
    match = models.CharField(max_length=45)
    recommended_dscp = models.CharField(max_length=45)
    delay_ref = models.CharField(max_length=45)
    loss_ref = models.CharField(max_length=45)

    @property
    def priority(self):
        if self.recommended_dscp.startswith("a"):
            return self.recommended_dscp[2]

    @property
    def drop(self):
        if self.recommended_dscp.startswith("a"):
            return self.recommended_dscp[3]

    @property
    def __str__(self):
        return self.name


class Policy(models.Model):
    name = models.CharField(max_length=45, unique=True, error_messages={'unique': 'this name is in used'})
    description = models.CharField(max_length=45)
    enable = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class PolicyIn(models.Model):
    policy_ref = models.ForeignKey(Policy, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    @property
    def name(self):
        return self.policy_ref.name

    @property
    def description(self):
        return self.policy_ref.description

    @property
    def render_policy(self):
        env = Environment(loader=FileSystemLoader(str(MEDIA_ROOT[0]) + "/monitoring_conf/"))
        classes = Application.objects.filter(policy_in_id=self.id)
        named = env.get_template("policyIn.j2")
        config_file = named.render(classes=classes, a=self)
        config = config_file.splitlines()
        # driver = napalm.get_network_driver('ios')
        # device = driver(hostname='192.168.5.1', username='admin',
        #                 password='admin')
        #
        # print('Opening ...')
        # device.open()
        # print('Loading replacement candidate ...')
        # device.load_merge_candidate(config=config_file)
        # print('\nDiff:')
        # print(device.compare_config())
        # print('Committing ...')

        return config_file


class PolicyOut(models.Model):
    policy_ref = models.ForeignKey(Policy, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    @property
    def name(self):
        # interface = Interface.objects.get(policy_out_ref=self)
        interfaces = Interface.objects.all()
        for i in interfaces:
            if i.policy_out_ref == self:
                return "OUT_{}_{}".format(self.policy_ref.name, i.interface_name)

    @property
    def description(self):
        return self.policy_ref.description

    @property
    def render_policy(self):
        env = Environment(loader=FileSystemLoader(str(MEDIA_ROOT[0]) + "/monitoring_conf/"))
        groups = Group.objects.filter(policy=self.policy_ref)
        regroupement_classes = RegroupementClass.objects.filter(policy_out_id=self.id)
        dscp_list = Dscp.objects.all()
        classes = Application.objects.all()
        named = env.get_template("policyOut.j2")
        config_file = named.render(groups=groups, classes=classes, a=self, regroupement_classes=regroupement_classes,
                                   dscp_list=dscp_list)
        return config_file

    @property
    def service_policy(self):
        interface = Interface.objects.get(policy_out_ref=self)
        env = Environment(loader=FileSystemLoader(str(MEDIA_ROOT[0]) + "/monitoring_conf/"))
        output = env.get_template("service_policy.j2")
        config_file = output.render(interface=interface)
        return config_file


class Policing(models.Model):
    cir = models.CharField(max_length=45)
    pir = models.CharField(max_length=45)
    dscp_transmit = models.CharField(max_length=45)


class Shaping(models.Model):
    peak = models.CharField(max_length=45)
    average = models.CharField(max_length=45)


class Group(models.Model):
    name = models.CharField(max_length=45)
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE, null=True)
    priority = models.CharField(max_length=45)


class RegroupementClass(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    policing = models.ForeignKey(Policing, on_delete=models.CASCADE, null=True)
    shaping = models.ForeignKey(Shaping, on_delete=models.CASCADE, null=True)
    policy_out = models.ForeignKey(PolicyOut, on_delete=models.CASCADE, null=True)
    bandwidth = models.CharField(max_length=45)
    priority = models.CharField(max_length=45)

    def __str__(self):
        return self.name

    @property
    def name(self):
        return self.group.name


class Dscp(models.Model):
    dscp_value = models.CharField(max_length=45)
    regroupement_class = models.ForeignKey(RegroupementClass, on_delete=models.CASCADE, null=True)
    drop_min = models.CharField(max_length=45)
    drop_max = models.CharField(max_length=45)
    denominator = models.CharField(max_length=45)



class Application(models.Model):
    # Low, Med, High = "1", "2", "3"
    # DROP = (
    #     (Low, "1"),
    #     (Med, "2"),
    #     (High, "3")
    # )
    # Low, Med, High, Priority = "1", "2", "3", "4"
    # PRIORITY = (
    #     (Low, "1"),
    #     (Med, "2"),
    #     (High, "3"),
    #     (Priority, "4")
    # )
    EF, AF43, AF42, AF41, AF33, AF32, AF23, AF21 = "EF", "AF43", "AF42", "AF41", "AF33", "AF32", "AF23", "AF21"
    DSCP = ((EF, "EF"),
            (AF43, "AF43"),
            (AF42, "AF42"),
            (AF41, "AF41"),
            (AF33, "AF33"),
            (AF32, "AF32"),
            (AF23, "AF23"),
            (AF21, "AF21"))

    IP, TCP, UDP, TCP_UDP = "ip", "tcp", "udp", "tcp/udp"
    PROTOCOL = (
        (IP, "ip"),
        (TCP, "tcp"),
        (UDP, "udp"),
        (TCP_UDP, "tcp/udp")
    )

    business_type = models.ForeignKey(BusinessType, on_delete=models.CASCADE, null=True)
    business_app = models.ForeignKey(BusinessApp, on_delete=models.CASCADE, null=True)
    policy_in = models.ForeignKey(PolicyIn, on_delete=models.CASCADE, null=True)
    # app_priority = models.CharField(max_length=20, choices=PRIORITY)
    # drop_prob = models.CharField(max_length=20, choices=DROP)
    mark = models.CharField(max_length=20, choices=DSCP)
    dscp = models.ForeignKey(Dscp, on_delete=models.CASCADE, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    source = models.CharField(max_length=45)
    destination = models.CharField(max_length=45)
    begin_time = models.CharField(max_length=45, default="00:00")
    end_time = models.CharField(max_length=45, default="24:00")
    protocol_type = models.CharField(max_length=45, choices=PROTOCOL, default=IP)
    port_number = models.CharField(max_length=45)
    custom_name = models.CharField(max_length=45)

    def __str__(self):
        return self.name

    @property
    def name(self):
        if self.business_app is not None:
            return "{}".format(self.business_app.name)
        if self.custom_name is not None:
            return self.custom_name

    @property
    def category(self):
        if self.business_app is not None:
            return "{}".format(self.business_type.name)
        if self.custom_name is not None:
            return "custom"

    @property
    def match(self):
        if self.business_app is not None:
            return "{}".format(self.business_app.match)
        else:
            return None

    @property
    def dscp_value(self):
        if self.mark != '':
            return self.mark
        else:
            return self.business_app.recommended_dscp

    @property
    def app_priority(self):
        if self.mark.startswith("A"):
            return self.mark[2]
        elif self.business_app is not None:
            return self.business_app.priority
        else:
            return None

    @property
    def drop_prob(self):
        if self.mark.startswith("A"):
            return self.mark[3]
        elif self.business_app is not None:
            return self.business_app.drop
        else:
            return None

    @property
    def time_range(self):
        if self.begin_time != '':
            if self.end_time != '':
                return "{}_time_range".format(self.name)
        else:
            return None

    @property
    def acl_name(self):
        return "{}_acl".format(self.name)

    @property
    def render_time_range(self):
        env = Environment(loader=FileSystemLoader(str(MEDIA_ROOT[0]) + "/monitoring_conf/"))
        output = env.get_template("time.j2")
        config_file = output.render(a=self)

        return config_file

    @property
    def acl_list(self):
        source = ''
        source_wild_card = ''
        destination = ''
        destination_wild_card = ''
        if self.source != 'any':
            source = IPNetwork(self.source)
            print(source)
            source_wild_card = source.hostmask.ipv4()
        if self.destination != 'any':
            destination = IPNetwork(self.destination)
            destination_wild_card = destination.hostmask.ipv4()

        env = Environment(loader=FileSystemLoader(str(MEDIA_ROOT[0]) + "/monitoring_conf/"))
        output = env.get_template("acl.j2")
        config_file = output.render(source_wild_card=source_wild_card,
                                    destination_wild_card=destination_wild_card,
                                    source=source,
                                    destination=destination,
                                    a=self)

        return config_file


class Access(models.Model):
    management_interface = models.CharField(max_length=45)
    management_address = models.CharField(max_length=45)
    username = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    enable_secret = models.CharField(max_length=45)


class Device(models.Model):
    hostname = models.CharField(max_length=45)
    management = models.ForeignKey(Access, on_delete=models.CASCADE, null=True)
    topology_ref = models.ForeignKey(Topology, on_delete=models.CASCADE, null=True)
    policy_ref = models.ForeignKey(Policy, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.hostname

    def netmiko_connect(self):
        return ConnectHandler(device_type="cisco_ios", ip=self.management.management_address,
                              username=self.management.username, password=self.management.password)

    def connect(self):
        driver = get_network_driver("ios")
        device = None
        try:
            device = driver(self.management.management_address, self.management.username,
                            self.management.password)
            device.open()
        except Exception as e:
            print(e)
        return device

    def enable_nbar(self):
        interfaces = Interface.objects.filter(device_ref=self)
        env = Environment(loader=FileSystemLoader(str(MEDIA_ROOT[0]) + "/monitoring_conf/"))
        output = env.get_template("protocol_discovery.j2")
        config_file = output.render(interfaces=interfaces)
        connection = self.connect()
        try:
            connection.load_merge_candidate(config=config_file)
            connection.commit_config()
            connection.close()
            return True
        except Exception as e:
            print(e)
            connection.close()
            return False

    def discovery_application(self):
        list_app = []
        interfaces = Interface.objects.filter(device_ref=self)
        connection = self.netmiko_connect()
        print("opening......")
        for interface in interfaces:
            try:
                cmd = "show ip nbar protocol-discovery interface " + interface.interface_name
                print(cmd)
                file = connection.send_command(
                    "show ip nbar protocol-discovery interface " + interface.interface_name).splitlines()
                print(file)

                p = False
                for line in file:
                    if p or "-------------------" in line:
                        p = True

                        k = line.split()
                        for a in k:
                            if a.isdigit():
                                break
                            if "----" in a:
                                break
                            if "unknown" in a:
                                break
                            if "Total" in a:
                                break
                            else:
                                list_app.append(a)
            except Exception as e:
                print(e)
        return set(list_app)

    def ingress(self):
        interfaces = Interface.objects.filter(ingress=True, device=self)
        if interfaces is not None:
            return True
        else:
            return False

    def egress(self):
        interfaces = Interface.objects.filter(egress=True, device=self)
        if interfaces is not None:
            return True
        else:
            return False

    def service_policy(self):
        interfaces = Interface.objects.filter(device_ref=self)
        policy_in = PolicyIn.objects.get(policy_ref=self.policy_ref)
        env = Environment(loader=FileSystemLoader(str(MEDIA_ROOT[0]) + "/monitoring_conf/"))
        output = env.get_template("service_policy.j2")
        config_file = output.render(interfaces=interfaces, policy_in=policy_in)
        return config_file


class Interface(models.Model):
    interface_name = models.CharField(max_length=45)
    ingress = models.BooleanField(default=True)
    device_ref = models.ForeignKey(Device, on_delete=models.CASCADE, null=True)
    egress = models.BooleanField(default=False)

    policy_out_ref = models.ForeignKey(PolicyOut, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.interface_name
