from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

from .models import Device

# 开机操作

# /device/[key]/start/
# 判断是否关机状态

# /device/[key]/close/
# 判断是否开机状态

# /device/[key]/stats/
# 查询设备状态

# post
# code
class SignIn(View):
    http_method_names = ['post', 'head', 'options']

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(SignIn, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        """ HTTP response 200 to allow, 403 in other case
        see function sensor.mosquitto.auth_plugin.utils.has_permission

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        data = {}

        # username => openid
        # password => null

        # force_login

        if hasattr(request, 'POST'):
            data = request.POST
        elif hasattr(request, 'DATA'):  # pragma: no cover
            data = request.DATA

        try:
            device = Device.objects.filter(appkey=data.get('username'), secret=data.get('password'), is_active=True)
            if device:
                return HttpResponse('')
        except Device.DoesNotExist:
            return HttpResponseForbidden('')


class Device(View):
    http_method_names = ['post', 'head', 'options']

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(Acl, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        """ HTTP response 200 to allow, 403 in other case
        see function sensor.mosquitto.auth_plugin.utils.has_permission

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        data = {}

        if hasattr(request, 'POST'):
            data = request.POST
        elif hasattr(request, 'DATA'):  # pragma: no cover
            data = request.DATA

        try:
            device = Device.objects.filter(appkey=data.get('username'), secret=data.get('password'), is_active=True)
            if device:
                return HttpResponse('')
        except Device.DoesNotExist:
            return HttpResponseForbidden('')

