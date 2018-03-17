# coding=utf-8
import json
import serial
from . import MODELS

class Sensor:

    def __init__(self, model='01' , port='/dev/tty.SLAB_USBtoUART', rate=9600):
        self.serial = serial.Serial(port, rate)
        self.models = MODELS.get(model, None)
s
    def __getitems__(self, item):
        self.serial.write(self.models.get(item))
      