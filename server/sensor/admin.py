from django.contrib import admin
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe
from sensor import models


class AclAdmin(admin.ModelAdmin):
    search_fields = ('topic__name',)
    list_filter = ('acc', 'allow',)
    ordering = ('topic',)
    list_display = ('topic', 'allow', 'acc', 'password')


class TopicAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_filter = ('dollar', 'wildcard',)
    list_display = ('name', 'dollar', 'wildcard')


class ClientIdAdmin(admin.ModelAdmin):
    search_fields = ('name',)


class DeviceAdmin(admin.ModelAdmin):

    def preview(self, obj):
        return mark_safe("<span style='color: blue;font-weight: bold;'>%s</span>" % obj.get_status_display())
        # return mark_safe("<span style='color: green;font-weight: bold;'>%s</span>" % obj.get_status_display())
        # return mark_safe("<span style='color: red;font-weight: bold;'>%s</span>" % obj.get_status_display())

    preview.short_description = '状态'
    
    date_hierarchy = 'created'
    list_display = ('appkey', 'name', 'model', 'preview')

class DeviceModelAdmin(admin.ModelAdmin):
    list_display = ('name',)


class RecordsAdmin(admin.ModelAdmin):
    list_display = ('member', 'device', 'created', 'status')

    def has_add_permission(self, request):
        pass

    # def has_change_permission(self, request, obj=None):
    #     pass


# admin.site.register(models.ACL, AclAdmin)
# admin.site.register(models.Topic, TopicAdmin)
admin.site.register(models.Device, DeviceAdmin)
admin.site.register(models.Records, RecordsAdmin)
# admin.site.register(models.ClientId, ClientIdAdmin)
admin.site.register(models.DeviceModel, DeviceModelAdmin)
