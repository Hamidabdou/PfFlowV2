from rest_framework_mongoengine import serializers
from QoSmonitor.models import *
from django.contrib.auth.models import User, Group
from rest_framework import serializers as sr
from napalm import get_network_driver

from QoSmanager.models import *


class accessSerializer(serializers.EmbeddedDocumentSerializer):
    class Meta:
        model = access
        fields = "__all__"


class deviceSerializer(serializers.DocumentSerializer):
    management = accessSerializer(many=False)
    topology_name = sr.CharField()

    def validate(self, value):
        management = value['management']
        addr = management["management_address"]
        user = management["username"]
        passwd = management['password']
        driver = get_network_driver("ios")
        device = driver(addr, user, passwd, timeout=10)
        try:
            device.open()
            device.close()
            return value
        except Exception as e:
            raise sr.ValidationError(e)

    class Meta:
        model = device
        fields = ["management", "topology_name"]


class topologySerializer(serializers.DocumentSerializer):
    class Meta:
        model = topology
        fields = ["topology_name", "topology_desc"]


class deviceListSerializer(serializers.DocumentSerializer):
    management = accessSerializer(many=False)

    class Meta:
        model = device
        fields = "__all__"


class statSerializer(serializers.DocumentSerializer):
    management = accessSerializer(many=False)

    class Meta:
        model = netflow_fields
        fields = "__all__"


class discover_networkSerializer(sr.Serializer):
    topology = sr.CharField()


class configure_monitoringSerializer(sr.Serializer):
    destination = sr.CharField()
    topology = sr.CharField()


class start_monitoringSerializer(sr.Serializer):
    topology = sr.CharField()


class preapare_envSerializer(sr.Serializer):
    topology = sr.CharField()


class UserSerializer(sr.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class GroupSerializer(sr.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class ApplicationSerializer(sr.HyperlinkedModelSerializer):
    app_name = sr.ReadOnlyField(source='name')
    app_category=sr.ReadOnlyField(source='category')

    class Meta:
        model = Application
        fields = ['id','app_name','app_category','app_priority','drop_prob','mark']

    def update(self, instance, validated_data):
        print(validated_data)
        instance.mark = validated_data.get('mark', instance.mark)
        print(instance.app_priority)
        if instance.mark=="EF":
            instance.group = Group.objects.get(priority="EF", policy_id=instance.group.policy)
        else:
            instance.group= Group.objects.get(priority=instance.app_priority, policy_id=instance.group.policy)
        print(instance.group.id)
        instance.save()

        return instance