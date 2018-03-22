# -*- coding: utf-8 -*-


from django.conf import settings
from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from suit.admin import SortableModelAdmin
from wechatpy import WeChatClient

from .models import (DBTextMsg, PatternT2T, DBImgTextMsg, PatternT2PT, PatternE2PT, PatternE2T, Member, WechatMenu)


class PatternE2PTAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'event', 'event_key',)
    list_filter = ('event', 'type')


class WechatMenuAdmin(MPTTModelAdmin, SortableModelAdmin):
    mptt_level_indent = 20
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug', 'is_active')
    list_editable = ('is_active',)
    list_display_links = ('name',)
    sortable = 'order'

    def conditional(self, queryset):
        conditional = {
            "button": [
                {
                    "type": "click",
                    "name": "今日歌曲",
                    "key": "V1001_TODAY_MUSIC"
                },
                {
                    "type": "click",
                    "name": "歌手简介",
                    "key": "V1001_TODAY_SINGER"
                },
                {
                    "name": "菜单",
                    "sub_button": [
                        {
                            "type": "view",
                            "name": "搜索",
                            "url": "http://www.soso.com/"
                        },
                        {
                            "type": "view",
                            "name": "视频",
                            "url": "http://v.qq.com/"
                        },
                        {
                            "type": "click",
                            "name": "赞一下我们",
                            "key": "V1001_GOOD"
                        }
                    ]
                }
            ],
            "matchrule": {
                "group_id": "",
                "sex": "",
                "country": "中国",
                "province": "",
                "city": "",
                "client_platform_type": ""
            }
        }

        rows = WechatMenu.objects.order_by('order').filter(parent=None)
        button = []

        for row in rows:
            child = row.get_children()
            menus = {
                'name': row.name,
            }

            if not child:
                if row.type == 'click':
                    menus['key'] = row.key
                else:
                    menus['url'] = row.key

                menus['type'] = row.type

            if child:
                for itme in child:
                    sub_button = {
                        'name': itme.name,
                        'type': itme.type,
                    }

                    if itme.type == 'click':
                        sub_button['key'] = itme.key
                    else:
                        sub_button['url'] = itme.key

                    menus['sub_button'] = []
                    menus['sub_button'].append(sub_button)

            button.append(menus)

        conditional['button'] = button
        return conditional

    def make_publish(self, request, queryset):
        self.conditional(queryset)
        client = WeChatClient(settings.APPKEY, settings.SECRET)
        client.menu.add_conditional(self.conditional(queryset))

        self.message_user(request, "成功发布菜单.")

    make_publish.short_description = "发布所选菜单"

    actions = [make_publish, 'delete_selected']


class PatternT2PTAdmin(admin.ModelAdmin):
    list_display = ('name', 'type',)
    list_filter = ('type',)


class MemberAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'openid', 'mobile',)


# class TermAdmin(admin.ModelAdmin):
#     search_fields = ('keyword',)


admin.site.register(PatternE2PT, PatternE2PTAdmin)
admin.site.register(PatternE2T, PatternE2PTAdmin)

admin.site.register(PatternT2PT, PatternT2PTAdmin)
admin.site.register(PatternT2T, PatternT2PTAdmin)

admin.site.register(DBTextMsg)
admin.site.register(DBImgTextMsg)
admin.site.register(Member, MemberAdmin)
# admin.site.register(Term, TermAdmin)
admin.site.register(WechatMenu, WechatMenuAdmin)
