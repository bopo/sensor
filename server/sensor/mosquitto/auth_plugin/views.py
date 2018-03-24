import hashlib

from django.contrib.auth import authenticate, get_user_model
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

from sensor.models import ACL, PROTO_MQTT_ACC, Device, Topic

from .auth import has_permission


def check_signature(username=None, password=None, secret=None):
    """Verify if the author of received msg is tencent."""

    if username and secret and password:
        tmplist = sorted([username, secret])
        newtext = ''.join(tmplist).encode('utf-8')
        results = hashlib.sha1()
        results.update(newtext)

        if results.hexdigest() == str(password):
            return True
        else:
            return False
    
    return False


class Auth(View):
    http_method_names = ['post', 'head', 'options']

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(Auth, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        """ HTTP response 200 to allow, 403 in other case
        Access if exist ACL with:
            - ACC, TOPIC and PASSWORD not matter the user
            - USERNAME and PASSWORD for an existing active user and with topic and acc

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

        topics = Topic.objects.filter(name=data.get('topic'))

        try:
            acc = int(data.get('acc', None))
        except:
            acc = None

        allow = True

        if topics.exists() and acc in dict(PROTO_MQTT_ACC).keys():
            topic = topics.get()
            acls = ACL.objects.filter(acc=acc, topic=topic,
                                      password__isnull=False, password=data.get('password'))
            if acls.exists():
                allow = True

        if not allow:
            user = authenticate(username=data.get('username'), password=data.get('password'))
            allow = has_permission(user, data.get('topic', '#'), acc)

        if not allow:
            return HttpResponseForbidden('no')

        return HttpResponse('ok')


class Superuser(View):
    http_method_names = ['post', 'head', 'options']

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(Superuser, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """ HTTP response 200 to user exist and is_superuser, 403 in other case
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

        user_model = get_user_model()

        try:
            user = user_model.objects.get(username=data.get('username'), is_active=True)

            if user.is_superuser:
                return HttpResponse('ok')
        except user_model.DoesNotExist:
            pass

        return HttpResponseForbidden('no')


class Acl(View):
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

        username = data.get('username')
        password = data.get('password')

        try:
            device = Device.objects.filter(appkey=username, is_active=True).get()
            verify = check_signature(username, password, device.secret)
            
            if verify:
                return HttpResponse('ok')
            else:
                return HttpResponseForbidden('no')
        except Device.DoesNotExist:
            return HttpResponseForbidden('no')
