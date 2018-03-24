import json
import logging
import threading

import paho.mqtt.client as mqtt
from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext_lazy as _

from sensor.models import Device

logger = logging.getLogger('server')


class MQTTServer:
    client = mqtt.Client()

    def __init__(self, host, port, debug=False, tls=True):
        self._host = host
        self._port = int(port)

        self.client.reinitialise(client_id='master', clean_session=True, userdata=None)

        if tls is True:
            self.client.tls_set(ca_certs='./.certs')

        if debug is True:
            self.client.on_log = self._on_log
            logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)s %(levelname)s %(message)s')

        self.client.on_connect = self._on_connect  # 设置连接上服务器回调函数
        self.client.on_message = self._on_message  # 设置接收到服务器消息回调函数

    def _on_log(self, mqttc, obj, level, string):
        logger.info("Log: %s" % string)

    def connect(self, appkey='master', secret='master'):
        self.client.username_pw_set(appkey, secret)
        self.client.connect(self._host, self._port, 60)  # 连接服务器,端口为1883,维持心跳为60秒

    def publish(self, topic, data):
        self.client.publish(topic, data)
        logger.debug('publish: ' + topic + data)

    def loop(self, timeout=None):
        thread = threading.Thread(target=self._loop, args=(timeout,))
        thread.start()

    def _loop(self, timeout=None):
        if not timeout:
            self.client.loop_forever()
        else:
            self.client.loop(timeout)

    def _on_connect(self, client, userdata, flags, rc):
        logger.debug("Connected with result code " + str(rc))
        client.subscribe('master')

    def _on_message(self, client, userdata, message):  # 从服务器接受到消息后回调此函数
        logger.debug("主题:" + (str(message.topic)) + " 消息:" + (message.payload.decode()))

        try:
            status = json.loads(message.payload.decode()).get('status')
            appkey = json.loads(message.payload.decode()).get('appkey')
            device = Device.objects.get(appkey=appkey)
            device.status = status
            device.save()

            logger.debug("更新设备状态:" + appkey + " 状态:" + status)
        except Device.DoesNotExist:
            raise CommandError(str(_('Device not found')))


class Command(BaseCommand):
    help = str(_('Connect with client as subscriber, for test proposed'))

    def add_arguments(self, parser):
        parser.add_argument('topic', action='store',
                            type=str, default=None,
                            help=str(_('Subcribe topic'))
                            )

        parser.add_argument('--qos', action='store',
                            type=int, default=0, dest='qos',
                            help=str(_('Quality of Service'))
                            )

        parser.add_argument('--debug', action='store',
                            type=bool, default=False, dest='debug',
                            help=str(_('Debug of Service'))
                            )
        parser.add_argument('--tls', action='store',
                            type=bool, default=False, dest='tls',
                            help=str(_('tls of On'))
                            )

    def handle(self, *args, **options):
        # if not options['topic']:
        #     raise CommandError(str(_('Topic requiered and must be only one')))

        client = MQTTServer(host='103.200.97.197', port=1883, tls=options['tls'], debug=options['debug'])
        client.connect()
        client.loop()
