#kivy.require('1.10.0')

import serial
import time
import multiprocessing

import kivy

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image

SERIAL_PORT = '/dev/cu.chusbserialfd130'
SERIAL_BAUDRATE = 115200

class Desktop(Widget):
    pass

class ArmApp(App):
    def build(self):
        return Desktop()

windows = ArmApp()
windows.run()