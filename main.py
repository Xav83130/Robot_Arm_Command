# kivy.require('1.10.0')

import serial
import time
import multiprocessing

import kivy

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image

# definition du port serie et du baudrate
SERIAL_PORT = '/dev/tty.wchusbserialfd130'
SERIAL_BAUDRATE = 115200


# connection au port serie
# ser = serial.Serial(SERIAL_PORT, SERIAL_BAUDRATE) #cette ligne suffit pour se connecter

# Quand j'appui sur le bouton "connection" je me connecte à l'arduino
class Desktop(Widget):
    pass


class ArmApp(App):
    def build(self):
        return Desktop()

    def connect(self):
        print("Je me connecte au port serie !!")
        self.serial = serial.Serial(SERIAL_PORT, SERIAL_BAUDRATE)
        time.sleep(2)  # Attend que GRBL s'initialise


windows = ArmApp()
windows.run()
