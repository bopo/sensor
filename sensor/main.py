import os
import time
import uuid
import json

import click
import environ

from client import MQTTClient
from server import MQTTServer
from sensor import UARTSensor

env = environ.Env()
env.read_env()

APPKEY = env('CLIENT_APPKEY', default='')
SECRET = env('CLIENT_SECRET', default='')

SERVER_HOST = env('SERVER_HOST', default='127.0.0.1')
SERVER_PORT = env('SERVER_PORT', default='1883')

SENSOR_PORT = env('SENSOR_PORT', default='/dev/tty.USB0')
SENSOR_RATE = env('SENSOR_RATE', default='9600')
SENSOR_MODE = env('SENSOR_MODE', default='0101')

@click.group()
@click.option('-v', '--verbose', count=True)
@click.pass_context
def cli(ctx, verbose):
    ctx.obj["VERBOSE"] = verbose

@cli.command(help='运行客户端')
@click.option('-d', '--debug', is_flag=True, help='调试模式.')
def client(debug=False):    
    print('APPKEY: ', APPKEY)
    print('SECRET: ', SECRET)
    print('')
    
    print('SERVER_HOST: ', SERVER_HOST)
    print('SERVER_PORT: ', SERVER_PORT)
    print('')

    client = MQTTClient(host=SERVER_HOST, port=SERVER_PORT, name=APPKEY, debug=debug)
    client.connect(APPKEY, SECRET)
    client.publish('master', '0000')
    client.loop()

    while True:
        client.publish('master', json.dumps([1,2,3]))
        time.sleep(1)   

@cli.command(help='运行服务端')
@click.option('-d', '--debug', is_flag=True, help='调试模式.')
def server(debug=False):
    print('>> server runing...')
    client = MQTTServer(host=SERVER_HOST, port=SERVER_PORT, debug=debug)
    client.connect(APPKEY, SECRET)
    client.loop()

    while True:
        update = json.dumps({'downurl':'http://www.baidu.com'})
        client.publish('update', str(update))
        time.sleep(2)  

@cli.command(help='检查系统状态')
@click.option('-d', '--debug', is_flag=True, help='调试模式.')
def doctor(debug=False):
    sensor = UARTSensor(port=SENSOR_PORT, rate=SENSOR_RATE, mode=SENSOR_MODE)
    client = MQTTClient(host=SERVER_HOST, port=SERVER_PORT, name=APPKEY, debug=debug)
    
    print('[+] UART checking ...', end=" ")
    print('ok') if sensor.connect() else print('no')

    # print('[+] MODE checking ...', end=" ")
    # print('ok') if sensor.verify('mode') else print('no')

    print('[+] MQTT checking ...', end=" ")
    print('ok') if client.connect() else print('no')

def main():
    cli(obj={})

if __name__ == '__main__':
    main()
