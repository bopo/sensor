# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

MSG_TYPES = (
    ('text', '文本消息'),
    ('event', '事件消息'),
    ('image', '图片消息'),
    ('location', '位置消息'),
    ('voice', '语音消息'),
    ('video', '视频消息'),
)
EVENTS = (
    ('subscribe', '关注事件'),
    ('unsubscribe', '取消关注事件'),
    ('SCAN', '扫描二维码'),
    ('LOCATION', '上报地理位置'),
    ('CLICK', '自定义菜单事件'),
    ('VIEW', '用户点击链接的跳转事件'),
)


class WechatMenu(MPTTModel):
    TYPE_CHOICES = (('click', '点击'), ('view', '链接'))
    name = models.CharField(blank=True, max_length=50, verbose_name=_(u"名称"), help_text=u"可以为空，仅用来标识消息")
    slug = models.CharField(max_length=64, default='00')
    type = models.CharField(blank=True, max_length=50, verbose_name=_(u"类型"), choices=TYPE_CHOICES)
    key = models.CharField(blank=True, max_length=50, verbose_name=_(u"键值"), help_text=u"可以为空，仅用来标识消息")

    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', default='0')
    is_active = models.BooleanField()
    order = models.IntegerField()

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['order']
        parent_attr = 'parent'

    class Meta:
        verbose_name = u'微信菜单'
        verbose_name_plural = u'微信菜单'


class Member(TimeStampedModel):
    """msg in database"""

    openid = models.CharField(blank=True, max_length=50, verbose_name=_(u"openid"), help_text=u"不能为空", unique=True)
    mobile = models.CharField(_('手机号'), max_length=100, blank=True, null=True, default=None)
    verify = models.CharField(_('验证码'), max_length=100, blank=True, null=True)
    avatar = models.URLField(verbose_name=_('头像'))

    remark = models.CharField(_('微信备注'), max_length=100, blank=True, null=True)
    wechat = models.CharField(_('微信用户名'), max_length=100, blank=True, null=True)
    # wechat_nick = models.CharField(_('微信昵称'), max_length=100, blank=True, null=True)

    nickname = models.CharField(blank=True, max_length=50, verbose_name=_(u"昵称"), help_text=u"可以为空，仅用来标识消息")
    name = models.CharField(blank=True, max_length=50, verbose_name=_(u"姓名"), help_text=u"可以为空，仅用来标识消息")
    city = models.CharField(blank=True, max_length=50, verbose_name=_(u"城市"), help_text=u"可以为空，仅用来标识消息")
    country = models.CharField(blank=True, max_length=50, verbose_name=_(u"国家"), help_text=u"可以为空，仅用来标识消息")
    province = models.CharField(blank=True, max_length=50, verbose_name=_(u"省份"), help_text=u"可以为空，仅用来标识消息")
    language = models.CharField(blank=True, max_length=50, verbose_name=_(u"语言"), help_text=u"可以为空，仅用来标识消息")
    headimgurl = models.CharField(blank=True, max_length=200, verbose_name=_(u"头像"), help_text=u"可以为空，仅用来标识消息")
    unionid = models.CharField(blank=True, max_length=200, verbose_name=_(u"唯一标示"), help_text=u"可以为空，仅用来标识消息")
    subscribe_time = models.BigIntegerField(blank=True, verbose_name=_(u"关注事件"), null=True)
    groupid = models.IntegerField(blank=True, verbose_name=_(u"分组ID"), null=True)
    sex = models.SmallIntegerField(verbose_name=_('性别'), blank=True, null=True)

    def on_delete(self):
        pass

    def __str__(self):
        return u'%s %s' % (self.id, self.name)

    class Meta:
        verbose_name = u'微信会员管理'
        verbose_name_plural = u'微信会员管理'


class DBTextMsg(models.Model):
    """msg in database"""

    class Meta:
        verbose_name = u'回复管理(文字消息)'
        verbose_name_plural = u'回复管理(文字消息)'

    name = models.CharField(blank=True, max_length=50, verbose_name=u"消息名字", help_text=u"可以为空，仅用来标识消息")
    content = models.TextField(blank=False, verbose_name=u"消息内容")

    def on_delete(self):
        pass

    def __str__(self):
        return u'%s %s' % (self.id, self.name)


class DBImgTextMsg(models.Model):
    """image_text msg in database"""

    class Meta:
        verbose_name = u'回复管理(图文消息)'
        verbose_name_plural = u'回复管理(图文消息)'

    name = models.CharField(blank=True, max_length=50, verbose_name=u"消息名称", help_text=u"可以为空，仅用来标识消息")
    title = models.CharField(blank=True, max_length=255, verbose_name=u"消息标题")
    description = models.TextField(blank=True, verbose_name=u"消息描述")
    pic_url = models.URLField(blank=False, verbose_name=u"图片地址")
    url = models.URLField(blank=False, max_length=255, verbose_name=u"文章地址")

    def on_delete(self):
        pass

    def __str__(self):
        return u'%s %s' % (self.id, self.name)


class PatternE2T(models.Model):
    """text response pattern to user"""

    class Meta:
        verbose_name = u'回复规则(事件>文本消息)'
        verbose_name_plural = u'回复规则(事件>文本消息)'

    name = models.CharField(blank=True, max_length=50, verbose_name=u"规则命名",
        help_text=u"可以为空，仅用来标识规则")
    type = models.CharField(max_length=20,
        choices=MSG_TYPES, verbose_name=u"收到的消息类型(请保持默认)",
        default='event', )
    event = models.CharField(max_length=30,
        choices=EVENTS,
        default='CLICK', verbose_name=u"事件类型",
        help_text=u"除非收到的消息类型为“自定义菜单事件或者点击链接跳转事件，否则不要修改本字段”")
    event_key = models.CharField(blank=True, max_length=255,
        verbose_name=u"event_key或者自定义url",
        help_text=u'<strong>对于自定义菜单事件和自定义链接跳转事件这个是必填的！</strong>')
    handler = models.ForeignKey(DBTextMsg, verbose_name=u"回复消息", on_delete=models.CASCADE)

    def on_delete(self):
        pass

    def __str__(self):
        return u'%s %s' % (self.id, self.name)


class PatternE2PT(models.Model):
    """text response pattern to user"""

    class Meta:
        verbose_name = u'回复规则(事件>图文消息)'
        verbose_name_plural = u'回复规则(事件>图文消息)'

    name = models.CharField(blank=True, max_length=50, verbose_name=u"规则命名",
        help_text=u"可以为空，仅用来标识规则")
    type = models.CharField(max_length=20,
        choices=MSG_TYPES,
        default='event', verbose_name=u"用户消息类型(请保持默认)",
        help_text=u"除非你清楚这个字段的含义，否则请不要随意更改")
    event = models.CharField(max_length=30,
        choices=EVENTS,
        default='CLICK', verbose_name=u"事件类型")
    event_key = models.CharField(blank=True, max_length=255,
        verbose_name=u"event_key或者自定义url",
        help_text='<strong>对于自定义菜单事件和自定义链接跳转事件这个是必填的！</strong>')
    handler = models.ManyToManyField(
        DBImgTextMsg, verbose_name=u"回复消息", help_text=u"最多允许五条，不然会出错")

    def __str__(self):
        return u'%s %s' % (self.id, self.name)
    
    def on_delete(self):
        pass

class PatternT2PT(models.Model):
    """image_text response pattern to user"""

    class Meta:
        verbose_name = u'回复规则(文本>图文消息)'
        verbose_name_plural = u'回复规则(文本>图文消息)'

    name = models.CharField(blank=True, max_length=50, verbose_name=u"规则命名",
        help_text=u"可以为空，仅用来标识规则")
    type = models.CharField(max_length=20,
        choices=MSG_TYPES,
        default='text', verbose_name=u"用户消息类型(请保持默认)",
        help_text=u"除非你清楚这个字段的含义，否则请不要随意更改")
    content = models.CharField(max_length=50, blank=True, verbose_name=u"需要匹配的消息",
        help_text=u"使用正则表达式")
    handler = models.ManyToManyField(
        DBImgTextMsg, verbose_name=u"回复消息", help_text=u"最多允许五条，不然会出错")

    def on_delete(self):
        pass

    def __str__(self):
        return u'%s %s' % (self.id, self.name)


class PatternT2T(models.Model):
    """text response pattern to user"""

    class Meta:
        verbose_name = u'回复规则(文本>文本消息)'
        verbose_name_plural = u'回复规则(文本>文本消息)'

    name = models.CharField(blank=True, max_length=50, verbose_name="规则命名",
        help_text=u"可以为空，仅用来标识规则")
    type = models.CharField(max_length=20,
        choices=MSG_TYPES,
        default='text', verbose_name=u"用户消息类型(请保持默认)",
        help_text=u"除非你清楚这个字段的含义，否则请不要随意更改")
    content = models.CharField(max_length=100, blank=True, verbose_name=u"收到的消息",
        help_text=u"使用正则表达式")
    handler = models.ForeignKey(DBTextMsg, on_delete=models.CASCADE, verbose_name=u"响应的消息内容")

    def on_delete(self):
        pass

    def __str__(self):
        return u'%s %s' % (self.id, self.name)
