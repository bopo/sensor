# coding=utf-8
import json
import serial
import environ

from models import MODELS

env = environ.Env()
env.read_env()

SENSOR_PORT = env('SENSOR_PORT', default='/dev/tty.USB0')
SENSOR_RATE = env('SENSOR_RATE', default='9600')
SENSOR_MODE = env('SENSOR_MODE', default='0101')

class UARTSensor:

    def __init__(self, port=SENSOR_PORT, rate=SENSOR_RATE, mode=SENSOR_MODE):
        # self.serial = serial.Serial(port, rate)
        self.models = MODELS.get(mode, None)
        # print(port, rate, mode)

    def reinitialise(self, *args, **kwargs):
        pass

    def connect(self, *args, **kwargs):
        try:
            self.serial = serial.Serial(SENSOR_PORT, SENSOR_RATE)
            return True
        except Exception as e:
            return False

    def publish(self, method, value=None):
        print('call', method, value)
        
        if value:
            print('value', self.models.get(method)['value'] % value)
        else:
            print('value', self.models.get(method)['value'])

        try:
            value = self.models.get(method) % value
            return self.serial.write(value)
        except Exception as e:
            return False

def main():
    sensor = UARTSensor()
    sensor.reinitialise()

    sensor.publish('start')
    sensor.publish('close')
    sensor.publish('stats')
    sensor.publish('clock', 10)

if __name__ == '__main__':
    main()     