from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from . import WeiMsg, check_signature
from .handlers import default_handler, router_patterns
from .routers import base_router, db_router
from django.conf import settings

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
        recv_msg = WeiMsg(request.body)

        for router in routers:
            result = router(recv_msg, router_patterns)

            if isinstance(result, HttpResponse):
                return result

        return default_handler(recv_msg)
