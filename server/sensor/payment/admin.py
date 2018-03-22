from django.contrib import admin

from .models import Wxorder, Wxpay


class WxorderAdmin(admin.ModelAdmin):
    list_display = ('out_trade_no', 'total_fee', 'pay_time')


admin.site.register(Wxpay)
admin.site.register(Wxorder, WxorderAdmin)
