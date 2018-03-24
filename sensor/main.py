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
env.read_env('env.sensor')

APPKEY = env('CLIENT_APPKEY', default='80e65000a9b4')
SECRET = env('CLIENT_SECRET', default='a4327198-2cd8-11e8-9dc8-80e65000a9b4')

SERVER_HOST = env('SERVER_HOST', default='103.200.97.197')
SERVER_PORT = env('SERVER_PORT', default='1883')

SENSOR_PORT = env('SENSOR_PORT', default='/dev/tty.USB0')
SENSOR_RATE = env('SENSOR_RATE', default='9600')
SENSOR_MODE = env('SENSOR_MODE', default='0101')
SENSOR_TLS = env('SENSOR_TLS', default=0)

@click.group()
@click.option('-v', '--verbose', count=True)
@click.pass_context
def cli(ctx, verbose):
    ctx.obj["VERBOSE"] = verbose

@cli.command(help='运行客户端')
@click.option('-d', '--debug', is_flag=True, help='调试模式.')
@click.option('--tls', is_flag=True, help='tls模式.')
def client(debug=False, tls=bool(SENSOR_TLS)):    
    print('APPKEY: ', APPKEY)
    print('SECRET: ', SECRET)
    print('')
    
    print('SERVER_HOST: ', SERVER_HOST)
    print('SERVER_PORT: ', SERVER_PORT)
    print('')

    client = MQTTClient(host=SERVER_HOST, port=SERVER_PORT, name=APPKEY, debug=debug, tls=tls)
    client.connect(APPKEY, SECRET)
    client.publish('master', '0000')
    client.loop()

    while True:
        client.publish('master', json.dumps({'status': 'cool', 'appkey': APPKEY}))
        time.sleep(1)   

@cli.command(help='运行服务端')
@click.option('-d', '--debug', is_flag=True, help='调试模式.')
@click.option('--tls', is_flag=True, help='tls模式.')
def server(debug=False, tls=bool(SENSOR_TLS)):
    print('>> Server runing...')
    client = MQTTServer(host=SERVER_HOST, port=SERVER_PORT, debug=debug, tls=tls)
    client.connect(APPKEY, SECRET)
    client.loop()

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
