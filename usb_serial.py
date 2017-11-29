# usb_serial.py

import serial
import serial.serialutil


from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.logger import Logger


def connect(self):

    Logger.info("Connecting to serial device: {} with baudrate: {}".format(
        self.root.ids.serialport.text,
        self.root.ids.baudrate.text))
    # int() est nécessaire car la valeur renvoyé par .text est une str, et le type attendu est un int
    try:
        self.serial = serial.Serial(self.root.ids.serialport.text,
                                    int(self.root.ids.baudrate.text))
#        time.sleep(2)  # Attend que GRBL s'initialise
#        self.root.serial.flushInput()  # vide la file d'attente série
    except serial.serialutil.SerialException as e:
        popup = Popup(title='System error',
                      size_hint=(None, None),
                      size=(400, 100),
                      content=Label(text="Can't connect to {}".format(
                          self.root.ids.serialport.text,
                          str(e)
                      ))
                      )
        popup.open()