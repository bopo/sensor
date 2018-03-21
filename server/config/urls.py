from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path
# from sensor import wechat, mosquitto

urlpatterns = [
	path('admin/', admin.site.urls),
    path('mqtt/', include('sensor.mosquitto.auth_plugin.urls')),
    # url(r'^admin/', include(admin.site.urls)),
    # url(r'^wechat/', include('sensor.wechat.urls')),
]
