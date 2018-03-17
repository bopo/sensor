# coding=utf-8
import json
import time
import threading
import paho.mqtt.client as mqtt
import logging

logger = logging.getLogger('sensor')

class MqttServer:
    client = mqtt.Client()

    def __init__(self, host, port, debug=False):
        self._host = host
        self._port = port

        if debug:
            try:
                import coloredlogs
                coloredlogs.install(level='DEBUG')
            except ImportError as e:
                logging.basicConfig(level = logging.DEBUG, format = '%(asctime)s %(name)s %(levelname)s %(message)s')

        self.client.reinitialise(client_id='master', clean_session=True, userdata=None)
        self.client.tls_set(ca_certs='.ca')
        self.client.on_connect = self._on_connect  # 设置连接上服务器回调函数
        self.client.on_message = self._on_message  # 设置接收到服务器消息回调函数

    def connect(self, appkey='master', secret='master'):
        self.client.username_pw_set(appkey, secret)
        self.client.connect(self._host, self._port, 60)  # 连接服务器,端口为1883,维持心跳为60秒

    def publish(self, topic, data):
        self.client.publish(topic, data)
        logger.debug('publish: ', topic, data)

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

    def _on_message(self, client, userdata, msg):  # 从服务器接受到消息后回调此函数
        logger.debug("主题:" + (str(msg.topic)) + " 消息:" + (msg.payload.decode()))
        topic = msg.payload.decode().split(':')[0]
        client.publish(topic, 'ok!')
        logger.debug(userdata)
     
if __name__ == '__main__':
    client = MqttServer('127.0.0.1', 1883)
    client.connect()
    client.loop()
