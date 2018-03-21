from django.urls import path
from . import views

urlpatterns = [
    path('acl', views.Acl.as_view(), name='mqtt_acl'),
    path('auth', views.Auth.as_view(), name='mqtt_auth'),
    path('superuser', views.Superuser.as_view(), name='mqtt_superuser'),
]
