from __future__ import unicode_literals

from django.apps import AppConfig


class SensorConfig(AppConfig):
    name = 'sensor'
    verbose_name = '设备管理'

    def ready(self):
        pass
