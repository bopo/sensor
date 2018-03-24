# -*- coding=utf-8 -*-
# Create your views here.
import time

from PAY_SERVICE.settings.base import APPID, PRIVATE_KEY_PATH, \
    ALI_PUB_KEY_PATH, ALIPAY_CALLBACK_URL, \
    WXAPPID, WX_PAY_KEY, WX_MCH_ID, WXPAY_CALLBACK_URL
from django.conf import settings
from jsonrpc import jsonrpc_method
from pay import utils
from pay.UUIDTools import UUIDTools
from pay.alipay import AliPay
from pay.models import Alipay, Wxpay, Wxorder
from pay.serializers import AlipaySerializer, WxpaySerializer
from pay.weixin_pay import UnifiedOrderPay, OrderQuery
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_xml.parsers import XMLParser
from rest_framework_xml.renderers import XMLRenderer

NOTIFY_URL = ALIPAY_CALLBACK_URL + 'api/v1.0/pay/alipay/notify/'


class AlipayViewSet(ModelViewSet):
    queryset = Alipay.objects.filter(is_active=True)
    serializer_class = AlipaySerializer

    @list_route(methods=['post'])
    def notify(self, request):
        """ 
            处理支付宝的notify_url
        :param request:
        :return:
        """
        processed_dict = {}

        for k, v in request.data.items():
            processed_dict[k] = v

        app_id = processed_dict.get('app_id')
        pay_no = processed_dict.get('out_trade_no')
        trade_no = processed_dict.get('trade_no')
        total_amount = processed_dict.get('total_amount')
        pay_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

        alipay = Alipay.objects.filter(pay_nos__contains=[pay_no]).values().first()

        if alipay is None:
            return Response("failed")

        if str(alipay.get('total_amount')) != str(total_amount):
            return Response("failed")

        if app_id != APPID:
            return Response("failed")

        if alipay.get('trade_no') != "":
            return Response("failed")

        sign = processed_dict.pop('sign', None)

        ali_pay = AliPay(
            appid=APPID,
            app_notify_url=NOTIFY_URL,
            app_private_key_path=PRIVATE_KEY_PATH,
            alipay_public_key_path=ALI_PUB_KEY_PATH,
            debug=True,  # 默认False,
            return_url=alipay.get('return_url')
        )

        is_verify = ali_pay.verify(processed_dict, sign)

        if is_verify is True:
            Alipay.objects.filter(pk=alipay.get('id')).update(pay_time=pay_time, trade_no=trade_no)
            ret = utils.request_thrift('TradingManager', 'notify',
                                       settings.TRADING_RPC_IP, int(settings.TRADING_RPC_PORT),
                                       alipay.get('out_trade_no'), str(pay_time))

            if ret == "success":
                return Response("success")


class WxpayViewSet(ModelViewSet):
    queryset = Wxpay.objects.filter(is_active=True)
    serializer_class = WxpaySerializer
    parser_classes = (XMLParser,)
    renderer_classes = (XMLRenderer,)


@jsonrpc_method('pay.get_alipay_url')
def get_alipay_url(request, subject, out_trade_no, total_amount, return_url, notify_url, user_id):
    recode = Alipay.objects.filter(out_trade_no=out_trade_no).values().first()
    if recode is not None:
        pay_no = UUIDTools.datetime_random()
        alipay = Alipay.objects.get(pk=recode.get('id'))
        alipay.pay_nos.append(pay_no)
        alipay.save()
    else:
        pay_no = out_trade_no
        Alipay.objects.create(subject=subject,
                              out_trade_no=out_trade_no,
                              total_amount=total_amount,
                              return_url=return_url,
                              notify_url=notify_url,
                              pay_nos=[pay_no],
                              created_by=user_id,
                              updated_by=user_id
                              )

    ali_pay = AliPay(
        appid=APPID,
        app_notify_url=NOTIFY_URL,
        app_private_key_path=PRIVATE_KEY_PATH,
        alipay_public_key_path=ALI_PUB_KEY_PATH,
        debug=True,  # 默认False,
        return_url=return_url
    )

    total_amount = "%.2f" % float(total_amount)
    url = ali_pay.direct_pay(
        subject=subject,
        out_trade_no=pay_no,
        total_amount=total_amount
    )
    # 沙箱环境网关
    # alipay_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
    # 正式环境网关
    alipay_url = "https://openapi.alipay.com/gateway.do?{data}".format(data=url)
    return alipay_url


@jsonrpc_method('pay.get_wxpay_url')
def get_wxpay_url(request, out_trade_no, body, total_fee, notify_url, product_id, user_id):
    recode = Wxorder.objects.filter(out_trade_no=out_trade_no).values().first()
    if recode is None:
        Wxorder.objects.create(
            out_trade_no=out_trade_no,
            body=body,
            total_fee=total_fee,
            notify_url=notify_url,
            product_id=product_id,
            created_by=user_id,
            updated_by=user_id
        )

    pay_no = UUIDTools.datetime_random()
    pay = UnifiedOrderPay(WXAPPID, WX_MCH_ID, WX_PAY_KEY)
    response = pay.post(body, pay_no, total_fee,
                        settings.WXPAY_CALLBACK_URL.split('://')[1].split(':')[0], settings.WX_NOTIFY_URL)

    if response and response["return_code"] == "SUCCESS" and response["result_code"] == "SUCCESS":
        wxorder = Wxorder.objects.filter(out_trade_no=out_trade_no).values().first()
        Wxpay.objects.create(
            out_trade_no=out_trade_no,
            pay_no=pay_no,
            code_url=response.get('code_url'),
            nonce_str=response.get('nonce_str'),
            created_by=user_id,
            updated_by=user_id
        )
        return response.get('code_url')


@jsonrpc_method('pay.wx_order_query')
def wx_order_query(request, out_trade_no):
    wxpays = Wxpay.objects.filter(out_trade_no=out_trade_no).values()
    pay = OrderQuery(WXAPPID, WX_MCH_ID, WX_PAY_KEY)

    for wxpay in wxpays:
        response = pay.post(wxpay.get('pay_no'))
        if response and response["return_code"] == "SUCCESS" \
                and response["result_code"] == "SUCCESS":
            trade_state = response["trade_state"]
            if trade_state == "SUCCESS":  # 支付成功
                pay_time = response["time_end"]
                transaction_id = response["transaction_id"]
                Wxorder.objects.filter(out_trade_no=out_trade_no).update(
                    pay_time=time.strftime("%Y-%m-%d %H:%M:%S",
                                           time.strptime(pay_time, "%Y%m%d%H%M%S")),
                    transaction_id=transaction_id
                )
                return {"success": True, "pay_time": pay_time}

    return {"success": False}
