# coding=utf-8
import json
import logging
import ssl
import threading
import hashlib
import time

import paho.mqtt.client as mqtt
import sensor as sens

logger = logging.getLogger('client')

class MQTTClient:
    client = mqtt.Client()
    sensor = sens.UARTSensor()
    
    def __init__(self, host='103.200.97.197', port=1883, name='sensor', mode='01', debug=False, tls=True):
        self._port = int(port)
        self._host = host
        self._name = name

        self.sensor.reinitialise(models_id=mode, return_status=False)
        self.client.reinitialise(client_id=name, clean_session=True, userdata=None)
        
        if tls == True:
            self.client.tls_set(ca_certs='./.certs')
        
        if debug == True:
            self.client.on_log = self._on_log
            logging.basicConfig(level = logging.DEBUG, format = '%(asctime)s %(name)s %(levelname)s %(message)s')

        self.client.on_connect = self._on_connect  # 设置连接上服务器回调函数
        self.client.on_message = self._on_message  # 设置接收到服务器消息回调函数

    def _on_log(self, mqttc, obj, level, string):
        logger.info("Log: %s" % string)

    def connect(self, appkey='sensor', secret='sensor'):
        passowrd = self._signature(appkey, secret)
        self.client.username_pw_set(appkey, passowrd)
        self.client.connect(self._host, self._port, 60)  # 连接服务器,端口为 1883,维持心跳为60秒

    def publish(self, topic, data):
        # data = '%s:%s' % (self._name, data)
        self.client.publish(topic, data)
        # logger.debug('publish: '+ topic +" "+ data)

    def loop(self, timeout=None):
        thread = threading.Thread(target=self._loop, args=(timeout,))
        thread.start()

    def _loop(self, timeout=None):
        if not timeout:
            self.client.loop_forever()
        else:
            self.client.loop(timeout)

    def _on_connect(self, client, userdata, flags, rc):
        # logger.debug("Connected with result code " + str(rc))
        client.subscribe('device/%s' % client._client_id.decode())
        client.subscribe('update')
        # logger.debug('subscribe '+ self._name)

    def _on_message(self, client, userdata, msg):  # 从服务器接受到消息后回调此函数
        logger.debug("主题: " + (str(msg.topic)) + " 消息: " + (msg.payload.decode()))

        # try:
        #     result = self.sensor.getattr(payload.get('method'))()
        #     client.publish('master', result)
        # except Exception as e:
        #     client.publish('master', 'method error.')

    def _signature(appkey=None, secret=None):
        if appkey and secret:
            tmplist = sorted([appkey, secret])
            newtext = ''.join(tmplist).encode('utf-8')
            results = hashlib.sha1()
            results.update(newtext)
            return results.hexdigest()
        
        return None

if __name__ == '__main__':
    client = MQTTClient(host='103.200.97.197', name='80e65000a9b4', port=1883, tls=False, debug=True)
    client.connect('80e65000a9b4', '80e65000a9b4')
    client.publish('master', '0000')
    client.loop()

    while True:
        client.publish('master', '0A00')
        time.sleep(1)    
