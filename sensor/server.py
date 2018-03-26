# coding=utf-8
import json
import time
import threading
import paho.mqtt.client as mqtt
import hashlib
import logging

logger = logging.getLogger('server')

class MQTTServer:
    client = mqtt.Client()

    def __init__(self, host, port, debug=False, tls=True):
        self._host = host
        self._port = int(port)

        self.client.reinitialise(client_id='master', clean_session=True, userdata=None)
        
        if tls == True:
            self.client.tls_set(ca_certs='./certs/ca.crt', 
                certfile='./certs/client.crt',
                keyfile='./certs/client.key')
        
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

    def _on_message(self, client, userdata, msg):  # 从服务器接受到消息后回调此函数
        logger.debug("主题:" + (str(msg.topic)) + " 消息:" + (msg.payload.decode()))
        topic = 'device/' + msg.payload.decode().split(':')[0]
        client.publish(topic, 'ok!')
        logger.debug(userdata)

    def _signature(self, appkey=None, secret=None):
        if appkey and secret:
            tmplist = sorted([appkey, secret])
            newtext = ''.join(tmplist).encode('utf-8')
            results = hashlib.sha1()
            results.update(newtext)
            return results.hexdigest()
        
        return None
             
if __name__ == '__main__':
    client = MQTTServer('127.0.0.1', 1883)
    client.connect()
    client.loop()

    while True:
        update = json.dumps({'downurl':'http://www.baidu.com'})
        client.publish('update', update)
        time.sleep(2)       
