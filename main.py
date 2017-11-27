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


class Desktop(Widget):
    pass


class ArmApp(App):
    def build(self):
        return Desktop()

    def connect(self): # connection au port serie
        print("Je me connecte au port serie !!")
        self.serial = serial.Serial(SERIAL_PORT, SERIAL_BAUDRATE)
        time.sleep(2)  # Attend que GRBL s'initialise
        self.serial.flushInput()  # vide la file d'attente série

    def disconnect(self): # deconnection au port serie
        print("Je me déconnecte du port serie !!")
        self.serial = serial.Serial = None

    def alarm(self): # Kill alarm lock
        print("Je retire l'alarme")
        self.serial.write("$X\r\n".encode('utf-8'))

    def x_move_pos(self): # move X+
        print("mouvement de X en positif")
        self.serial.write("G91X1\r\n".encode('utf-8'))

    def x_move_neg(self): # move X-
        print("mouvement de X en negatif")
        self.serial.write("G91X-1\r\n".encode('utf-8'))


windows = ArmApp()
windows.run()
