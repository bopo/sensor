#!/usr/bin/env python
# coding:utf-8
import json
import re

import requests
from django.http import HttpResponse
from wechatpy.replies import ArticlesReply

from .utils import text_response


def default_handler(recv_msg):
    return text_response(recv_msg, "没有匹配操作，返回默认信息")


def test_handler(recv_msg, *args, **kwargs):
    reply = ArticlesReply()
    reply.source = recv_msg.to_user_name
    reply.target = recv_msg.from_user_name
    reply.add_article({
        'title': '测试图文消息',
        'description': '图文消息描述',
        'image': 'http://pic1.win4000.com/pic/b/6e/5aee949474.jpg',
        'url': 'http://www.baidu.com'
    })
    reply.add_article({
        'title': '测试图文消息',
        'description': '图文消息描述',
        'image': 'http://pic1.win4000.com/pic/b/6e/5aee949474.jpg',
        'url': 'http://www.baidu.com'
    })

    xml = reply.render()
    return HttpResponse(xml)


def about_handler(recv_msg, *args, **kwargs):
    content = """
    关于我们
    """
    return text_response(recv_msg, content)


def help_handler(recv_msg, *args, **kwargs):
    content = """
    --键入小写命令--
    http://device.bopo.me/wechat/authorize
    """
    return text_response(recv_msg, content)


'''
    "subscribe": 1,
    "openid": "o6_bmjrPTlm6_2sgVt7hMZOPfL2M",
    "nickname": "Band",
    "sex": 1,
    "language": "zh_CN",
    "city": "广州",
    "province": "广东",
    "country": "中国",
    "headimgurl":    "http://wx.qlogo.cn/mmopen/g3MonUZtNHkdmzicIlibx6iaFqAc56vxLSUfpb6n5WKSYVY0ChQKkiaJSgQ1dZuTOgvLLrhJbERQQ4eMsv84eavHiaiceqxibJxCfHe/0",
   "subscribe_time": 1382694957,
   "unionid": " o6_bmasdasdsad6_2sgVt7hMZOPfL"
   "remark": "",
   "groupid": 0
'''


# def subscribe_handler(recv_msg, *args, **kwargs):
#     openid = recv_msg.from_user_name
#     member, status = Member.objects.get_or_create(openid=openid)
#
#     client = WeChatClient(settings.APPKEY, settings.SECRET)
#     user = client.user.get(openid)
#
#     for k, v in user.items():
#         if hasattr(member, k):
#             setattr(member, k, v)
#
#     member.save()
#
#     # client.message.send_text(openid, '股票最新走势,收到没')
#     content = """ -- """
#     return text_response(recv_msg, content)


def tuling_auto_reply(msg):
    tuling_key = '94921ef4597846b29674143a133e7158'

    if tuling_key:
        url = "http://www.tuling123.com/openapi/api"

        user_id = 're:'
        body = {'key': tuling_key, 'info': msg.encode('utf8'), 'userid': user_id}

        r = requests.post(url, data=body)

        respond = json.loads(r.text)
        result = ''

        if respond['code'] == 100000:
            result = respond['text'].replace('<br>', '  ')
        elif respond['code'] == 200000:
            result = respond['url']
        elif respond['code'] == 302000:
            for k in respond['list']:
                result = result + "【" + k['source'] + "】 " + \
                         k['article'] + "\t" + k['detailurl'] + "\n"
        else:
            result = respond['text'].replace('<br>', '  ')

        return result
    else:
        return "知道啦"


def tuling_handler(recv_msg, *args, **kwargs):
    content = tuling_auto_reply(recv_msg.content)
    return text_response(recv_msg, content)


router_patterns = [
    # 消息类型  消息文字（非文字类型消息留空）  操作函数
    ('text', re.compile(r'^help$'), help_handler),
    ('text', re.compile(r'^about$'), about_handler),
    ('text', re.compile(r'^test$'), test_handler),
    # ('text', re.compile(r'^\d{6}$'), stock_handler),
    # ('text', re.compile(r'^.*'), term_handler),
    ('text', re.compile(r'^.*'), tuling_handler),
    # ('event', re.compile(r'^subscribe$'), subscribe_handler),
]
