from model_utils import Choices
from rest_framework import serializers

from sensor.models import Device


class DeviceSerializer(serializers.ModelSerializer):
    interval = serializers.IntegerField(default=10, label='定时')
    switch = serializers.ChoiceField(default='', label='操作',
                                     choices=Choices(('await', '待机'), ('start', '开机'), ('close', '关机'),
                                                     ('clock', '定时')))

    class Meta:
        model = Device
        exclude = ('status_changed', 'appkey', 'secret', 'model', 'created', 'modified')
        read_only_fields = ('title', 'status')


class DeviceActionSerializer(DeviceSerializer):
    class Meta:
        model = Device
        exclude = ('status_changed', 'appkey', 'secret',)
        read_only_fields = ('title', 'status')
