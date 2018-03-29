import requests
from django.conf import settings
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


class LoginSerializer(serializers.Serializer):
    code = serializers.CharField(label='认证代码')
    data = serializers.CharField(label='加密数据', allow_blank=True)
    user = serializers.JSONField(label='用户数据', required=False, read_only=True)

    # {'session_key': 'xqVzM6XfjplVLG13cgxY1Q==', 'expires_in': 7200, 'openid': 'o04r80Pyr8A-A2BIVribYGijXpuQ'}

    def validate(self, attrs):
        print(attrs)
        server = settings.WXAPP_SERVER.format(APPKEY=settings.WXAPP_APPKEY, SECRET=settings.WXAPP_SECRET,
                                              JSCODE=attrs.get('code'))
        result = requests.get(server)
        print(server, result, result.json())

        if result:
            attrs['user'] = result.json()

        return attrs
