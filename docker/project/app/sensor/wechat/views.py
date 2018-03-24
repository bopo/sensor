from django.conf import settings
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from wechatpy import WeChatOAuth
from wechatpy.pay.api import  WeChatJSAPI

from . import WeiMsg, check_signature
from .handlers import default_handler, router_patterns
from .routers import base_router, db_router

routers = [base_router, db_router]


@csrf_exempt
def home(request):
    if request.method == 'GET':
        response = HttpResponse()

        if check_signature(request, settings.WECHAT_TOKEN):
            response.write(request.GET.get('echostr'))
            return response
        else:
            response.write('不提供直接访问！')
            return response

    if request.method == 'POST':
        print(request.body)
        recv_msg = WeiMsg(request.body.decode())

        for router in routers:
            result = router(recv_msg, router_patterns)

            if isinstance(result, HttpResponse):
                return result

        return default_handler(recv_msg)


def authorize(request, func):
    '''
    认证接口
    :param request:
    :return:
    '''
    code = request.GET.get('code', None)
    auth = WeChatOAuth(settings.WECHAT_APPKEY, settings.WECHAT_SECRET,
                       redirect_uri=request.build_absolute_uri(request.get_full_path()))

    if code is None:
        return HttpResponseRedirect(auth.authorize_url)

    access = auth.fetch_access_token(code)
    auth.refresh_access_token(access.get('refresh_token'))
    user = auth.get_user_info()

    return JsonResponse(user)


@authorize
def payment(request):
    '''
    支付接口

    :param request:
    :return:
    '''
    code = request.GET.get('code', None)
    auth = WeChatOAuth(settings.WECHAT_APPKEY, settings.WECHAT_SECRET,
                       redirect_uri=request.build_absolute_uri(request.get_full_path()))

    if code is None:
        return HttpResponseRedirect(auth.authorize_url)

    access = auth.fetch_access_token(code)
    auth.refresh_access_token(access.get('refresh_token'))
    user = auth.get_user_info()

    WeChatJSAPI()
    
    return JsonResponse(user)
