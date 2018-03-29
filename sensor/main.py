import os
import time
import uuid
import json

import click
import environ

from client import MQTTClient
from server import MQTTServer
from sensor import UARTSensor
from models import MACHINE

env = environ.Env()
env.read_env('env.sensor')

APPKEY = env('CLIENT_APPKEY', default='80e65000a9b4')
SECRET = env('CLIENT_SECRET', default='a4327198-2cd8-11e8-9dc8-80e65000a9b4')

SERVER_HOST = env('SERVER_HOST', default='103.200.97.197')
SERVER_PORT = env('SERVER_PORT', default='1883')

SENSOR_PORT = env('SENSOR_PORT', default='/dev/tty.USB0')
SENSOR_RATE = env('SENSOR_RATE', default='9600')
SENSOR_MODE = env('SENSOR_MODE', default='0101')
SENSOR_TLS  = env('SENSOR_TLS', default=1)

@click.group()
@click.option('-v', '--verbose', count=True)
@click.pass_context
def cli(ctx, verbose):
    ctx.obj["VERBOSE"] = verbose

@cli.command(help='运行客户端')
@click.option('-d', '--debug', is_flag=True, help='调试模式.')
@click.option('--tls', is_flag=True, help='tls模式.')
def client(debug=False, tls=False):    
    print('APPKEY: ', APPKEY)
    print('SECRET: ', SECRET)
    print('')
    
    print('SERVER_HOST: ', SERVER_HOST)
    print('SERVER_PORT: ', SERVER_PORT)
    print('')

    client = MQTTClient(host=SERVER_HOST, port=SERVER_PORT, name=APPKEY, debug=debug, tls=tls)
    client.connect(APPKEY, SECRET)
    client.publish('console', {'st': 'up', 'id': APPKEY})
    client.loop()

    while True:
        client.publish('console', json.dumps({'st': '00, 01, 02, 03', 'id': APPKEY}))
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

@cli.command(help='监测机器型号')
@click.option('-d', '--debug', is_flag=True, help='调试模式.')
@click.option('--nolog', is_flag=False, help='不显示日志.')
@click.option('--switch', default='stats', help='开关指令.')
def sensor(debug=False, nolog=False, switch='stats'):
    import glob
    ttys = glob.glob('/dev/tty.*')
    
    for k,v in enumerate(ttys):
        print(k,v)

    port = input('请输入端口:')
    # # rate = input('请输入速率:')
    # rate = 9600
    port = ttys[int(port)]
    # port = '/dev/tty.SLAB_USBtoUART'

    print(port)
    # print(rate)
    
    
    # client = MQTTClient(host=SERVER_HOST, port=SERVER_PORT, name=APPKEY, debug=debug)
    sensor = UARTSensor()

    # print('[+] UART checking ...')

    # for k, v in enumerate(ttys):
    #     sensor.reinitialise(port=v, rate=9600)

    #     if sensor.connect():
    #         print('[√] %d => %s ... ok' % (k, v))
    #     else:
    #         print('[x] %d => %s ... no' % (k, v))

    # port = input('请输入端口:')

    print('[+] MODE checking ...', end=" ")
    # for x in xrange(1,10):
    #     pass
    # sensor.reinitialise(port=v, rate=9600, mode=mode)
    # print('ok') if sensor.verify('mode') else print('no')
    
    for mode, _ in MACHINE.items():
        sensor.reinitialise(port=port, rate=9600, mode=mode)
        sensor.connect()
        # sensor.publish('start', debug=True)
        # input('press any key to continue.')
        # sensor.publish('close', debug=True)
        # input('press any key to continue.')
        sensor.publish(switch, debug=False)
        input('press any key to continue.')
        # sensor.publish('clock', debug=True)
        # input('press any key to continue.')

    # print('[+] MQTT checking ...', end=" ")
    # print('ok') if client.connect() else print('no')

def main():
    cli(obj={})

if __name__ == '__main__':
    main()
