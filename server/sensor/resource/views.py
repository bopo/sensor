# /device/[key]/stats/
# 查询设备状态
import json

from django.conf import settings
from rest_framework import mixins
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from sensor.models import Device
from sensor.sensor import MQTTServer
from .serializers import DeviceSerializer


# 开机操作
# /device/[key]/start/
# 判断是否关机状态
# /device/[key]/close/
# 判断是否开机状态

class DeviceViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin, GenericViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = (IsAuthenticated,)

    sensor = {}

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        return self.perform_action(serializer, instance)

    def perform_action(self, serializer, instance):
        interval = serializer.validated_data.get('interval')
        switch = serializer.validated_data.get('switch')
        action = json.dumps({'switch': switch, 'interval': interval})
        status = instance.status
        client = MQTTServer(settings.SERVER_HOST, settings.SERVER_PORT)
        client.connect()

        if status == 'busy' and switch != 'close':
            raise ValidationError({"detail": "设备正在使用中."})

        try:
            client.publish('device/%s' % instance.appkey, data=action)
            return Response({"detail": "操作已经顺利送达设备."})
        except Exception:
            raise ValidationError({"detail": "服务器异常错误."})
