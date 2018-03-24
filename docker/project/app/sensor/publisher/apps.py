from __future__ import unicode_literals

from django.apps import AppConfig


class PublisherConfig(AppConfig):
    name = 'sensor.publisher'
    verbose_name = '消息管理'

    def ready(self):
        pass
