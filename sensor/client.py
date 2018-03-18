# coding=utf-8
import json
import logging
import ssl
import threading
import time

import paho.mqtt.client as mqtt
import sensor as sens

logger = logging.getLogger('sensor')

class MQTTClient:
    client = mqtt.Client()
    sensor = sens.UARTSensor()
    
    def __init__(self, host='103.200.97.197', port=1883, name='sensor', mode='01', debug=False):
        self._port = int(port)
        self._host = host
        self._name = name

        if debug:
            try:
                import coloredlogs
                coloredlogs.install(level='DEBUG')
            except ImportError as e:
                logging.basicConfig(level = logging.DEBUG,format = '%(asctime)s %(name)s %(levelname)s %(message)s')

        self.sensor.reinitialise(models_id=mode, return_status=False)
        self.client.reinitialise(client_id=name, clean_session=True, userdata=None)
        self.client.tls_set(ca_certs='./.certs')
        self.client.on_connect = self._on_connect  # 设置连接上服务器回调函数
        self.client.on_message = self._on_message  # 设置接收到服务器消息回调函数

    def connect(self, appkey='sensor', secret='sensor'):
        self.client.username_pw_set(appkey, secret)
        self.client.connect(self._host, self._port, 60)  # 连接服务器,端口为 1883,维持心跳为60秒

    def publish(self, topic, data):
        data = '%s:%s' % (self._name, data)
        self.client.publish(topic, data)
        logger.debug('publish: '+ topic +" "+ data)

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
        client.subscribe(self._name)
        client.subscribe('update')
        logger.debug('subscribe '+ self._name)

    def _on_message(self, client, userdata, msg):  # 从服务器接受到消息后回调此函数
        logger.debug("主题: " + (str(msg.topic)) + " 消息: " + (msg.payload.decode()))

        # try:
        #     result = self.sensor.getattr(payload.get('method'))()
        #     client.publish('master', result)
        # except Exception as e:
        #     client.publish('master', 'method error.')
        
if __name__ == '__main__':
    client = MQTTClient(name='80e65000a9b4')
    client.connect('80e65000a9b4', '80e65000a9b4')
    client.publish('master', '0000')
    client.loop()

    while True:
        client.publish('master', '0A00')
        time.sleep(2)    
