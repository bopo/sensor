from django.urls import path
from . import views

urlpatterns = [
    path('getuser', views.Auth.as_view(), name='mqtt_auth'),
    path('aclcheck', views.Acl.as_view(), name='mqtt_acl'),
    path('superuser', views.Superuser.as_view(), name='mqtt_superuser'),
]
