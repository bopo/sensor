# coding=utf-8
import time
import json
import serial
import environ

from models import MACHINE


class UARTSensor:

    def __init__(self, port=None, rate=None, mode=None):
        self.mode = MACHINE.get(mode, None)
        self.port = port
        self.rate = rate

    def reinitialise(self, *args, **kwargs):
        for k,v in kwargs.items():
            if hasattr(self, k):
                if k == 'mode':
                    setattr(self, 'mode', MACHINE.get(v, None))
                else:
                    setattr(self, k, v)

    def connect(self, *args, **kwargs):
        try:
            self.serial = serial.Serial(self.port, self.rate, timeout=.5)
            return True
        except Exception as e:
            return False


    def publish(self, method='status', debug=False):
        res = self.mode.get(method)
        rev = self.push(res[0])

        print()
        print(self.mode.get('title'))
        print('======================')
        print('method:', method)
        print('cmmand:', res[0])
        print('return:', res[1])
        print('result:', rev)

        if rev:
            for x in res[1]:
                try:
                    if rev.decode() in x:
                        print('values:', res[1].index(x), '=>', x,'............ok')
                        return res[1].index(x)
                except ValueError as e:
                    pass

        print('values:', rev, '............no') 

        return None

    def push(self, value=None, default=None):
        if default:
            return default

        try:
            self.serial.write(bytes(value, encoding = "ascii"))
            time.sleep(.05)
            result = self.serial.read_all()
            print('writes:', value)
            print('result:', result)
            return result
        except Exception as e:
            raise e


def main():
    for mode, _ in MACHINE.items():
        print(mode)
        sensor = UARTSensor(mode=mode)
        sensor.reinitialise(mode=mode)
        sensor.publish('start', debug=True)
        input('press any key to continue.')
        sensor.publish('close', debug=True)
        input('press any key to continue.')
        sensor.publish('stats', debug=True)
        input('press any key to continue.')
        sensor.publish('clock', debug=True)
        input('press any key to continue.')

if __name__ == '__main__':
    main()     