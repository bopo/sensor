# /device/[key]/stats/
# 查询设备状态
import json

from django.conf import settings
from rest_framework import mixins, generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from sensor.models import Device
from sensor.sensor import MQTTServer
from .serializers import DeviceSerializer, LoginSerializer


class LoginViewSet(generics.CreateAPIView):
    """
    """
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeviceViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin, GenericViewSet):
    """
    """
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = (IsAuthenticated,)

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
