# -*- coding=utf-8 -*-
import hashlib
import re
import types
from random import Random

import requests
from django.core.exceptions import FieldDoesNotExist
from django.db import models
from django.db.models.fields.reverse_related import ForeignObjectRel
from .exception_handler import ForeignObjectRelDeleteError, ModelDontHaveIsActiveFiled, logger
from rest_framework.pagination import PageNumberPagination


def smart_str(s, encoding='utf-8', strings_only=False, errors='strict'):
    """
    Returns a bytestring version of 's', encoded as specified in 'encoding'.
    If strings_only is True, don't convert (some) non-string-like objects.
    """
    if strings_only and isinstance(s, (types.NoneType, int)):
        return s
    if not isinstance(s, str):
        try:
            return str(s)
        except UnicodeEncodeError:
            if isinstance(s, Exception):
                # An Exception subclass containing non-ASCII data that doesn't
                # know how to print itself properly. We shouldn't raise a
                # further exception.
                return ' '.join([smart_str(arg, encoding, strings_only,
                                           errors) for arg in s])
            return unicode(s).encode(encoding, errors)
    elif s and encoding != 'utf-8':
        return s.decode('utf-8', errors).encode(encoding, errors)
    else:
        return s


def format_url(params, api_key=None):
    url = "&".join(['%s=%s' % (key, smart_str(params[key])) for key in sorted(params)])
    if api_key:
        url = '%s&key=%s' % (url, api_key)
    return url


def calculate_sign(params, api_key):
    # 签名步骤一：按字典序排序参数, 在string后加入KEY
    url = format_url(params, api_key)
    # 签名步骤二：MD5加密, 所有字符转为大写
    return hashlib.md5(url.encode('utf-8')).hexdigest().upper()


def dict_to_xml(params, sign):
    xml = ["<xml>", ]
    for (k, v) in params.items():
        if (v.isdigit()):
            xml.append('<%s>%s</%s>' % (k, v, k))
        else:
            xml.append('<%s><![CDATA[%s]]></%s>' % (k, v, k))
    xml.append('<sign><![CDATA[%s]]></sign></xml>' % sign)
    return ''.join(xml)


def xml_to_dict(xml):
    if xml[0:5].upper() != "<XML>" and xml[-6].upper() != "</XML>":
        return None, None

    result = {}
    sign = None
    content = ''.join(xml[5:-6].strip().split('\n'))

    pattern = re.compile(r"<(?P<key>.+)>(?P<value>.+)</(?P=key)>")
    m = pattern.match(content)
    while (m):
        key = m.group("key").strip()
        value = m.group("value").strip()
        if value != "<![CDATA[]]>":
            pattern_inner = re.compile(r"<!\[CDATA\[(?P<inner_val>.+)\]\]>")
            inner_m = pattern_inner.match(value)
            if inner_m:
                value = inner_m.group("inner_val").strip()
            if key == "sign":
                sign = value
            else:
                result[key] = value

        next_index = m.end("value") + len(key) + 3
        if next_index >= len(content):
            break
        content = content[next_index:]
        m = pattern.match(content)

    return sign, result


def validate_post_xml(xml, appid, mch_id, api_key):
    sign, params = xml_to_dict(xml)
    if (not sign) or (not params):
        return None

    remote_sign = calculate_sign(params, api_key)
    if sign != remote_sign:
        return None

    if params["appid"] != appid or params["mch_id"] != mch_id:
        return None

    return params


def random_str(randomlength=8):
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    random = Random()
    return "".join([chars[random.randint(0, len(chars) - 1)] for i in range(randomlength)])


def post_xml(url, xml):
    return requests.post(url, data=xml.encode('utf-8'), verify=False)


class UnActiveModelMixin(object):
    """
    删除一个对象，并不真删除，级联将对应外键对象的is_active设置为false，需要外键对象都有is_active字段.
    """

    def perform_destroy(self, instance):
        rel_fileds = [f for f in instance._meta.get_fields() if isinstance(f, ForeignObjectRel)]

        links = [f.get_accessor_name() for f in rel_fileds]

        for link in links:
            manager = getattr(instance, link, None)
            if not manager:
                continue
            if isinstance(manager, models.Model):
                if hasattr(manager, 'is_active') and manager.is_active:
                    manager.is_active = False
                    manager.save()
                    raise ForeignObjectRelDeleteError(u'{} 上有关联数据'.format(link))
            else:
                if not manager.count():
                    continue
                try:
                    manager.model._meta.get_field('is_active')
                    manager.filter(is_active=True).update(is_active=False)
                except FieldDoesNotExist as ex:
                    # 理论上，级联删除的model上面应该也有is_active字段，否则代码逻辑应该有问题
                    logger.warn(ex)
                    raise ModelDontHaveIsActiveFiled(
                        '{}.{} 没有is_active字段, 请检查程序逻辑'.format(
                            manager.model.__module__,
                            manager.model.__class__.__name__
                        ))
        instance.is_active = False
        instance.save()

    def get_queryset(self):
        return self.queryset.filter(is_active=True)


class StandardResultsSetPagination(PageNumberPagination):
    page_size_query_param = 'size'
