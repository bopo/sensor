import click
import uuid
import time
from sensor.client import MqttClient
from sensor.server import MqttServer
import os

import environ

env = environ.Env()
env.read_env()

APPKEY = env('CLIENT_APPKEY', default='')
SECRET = env('CLIENT_SECRET', default='')

SERVER_HOST = env('SERVER_HOST', default='127.0.0.1')
SERVER_PORT = int(env('SERVER_PORT', default='1883'))

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

    client = MqttClient(host=SERVER_HOST, port=SERVER_PORT, name=APPKEY, debug=debug)
    client.connect(APPKEY, SECRET)
    client.publish('master', '0000')
    client.loop()

    while True:
        client.publish('master', '0A00')
        time.sleep(2)   

@cli.command(help='运行服务端')
@click.option('-d', '--debug', is_flag=True, help='调试模式.')
def server(debug=False):
    print('>> server runing...')
    client = MqttServer(host=SERVER_HOST, port=SERVER_PORT, debug=debug)
    client.connect()
    client.loop()

def main():
    cli(obj={})

if __name__ == '__main__':
    main()