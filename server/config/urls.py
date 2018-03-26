from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path
from sensor.wechat.views import home, authorize, payment

urlpatterns = [
	path('admin/', admin.site.urls),
    path('mqtt/', include('sensor.mosquitto.auth_plugin.urls')),
    path('api/', include('sensor.urls')),
    path('wechat/', home),
    path('wechat/authorize', authorize),
    path('wechat/payment', payment),
]
