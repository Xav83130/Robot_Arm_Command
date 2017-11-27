# kivy.require('1.10.0')

import serial
import serial.serialutil
import time

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.logger import Logger


class Desktop(Widget):
    pass


class ArmApp(App):
    def build(self):
        return Desktop()

    def idle(self): # change d'etat le Togglebutton ligne 64 du .kv
        # si je suis connecté au port serie
        # alors le bouton change d'etat 'state: down'
        pass

    def connect(self): # connection au port serie
        Logger.info("Connecting to serial device: {} with baudrate: {}".format(
                    self.root.ids.serialport.text,
                    self.root.ids.baudrate.text))
        # int() est nécessaire car la valeur renvoyé par .text est une str, et le type attendu est un int
        try:
            self.serial = serial.Serial(self.root.ids.serialport.text,
                                        int(self.root.ids.baudrate.text))

            time.sleep(2)  # Attend que GRBL s'initialise
            self.serial.flushInput()  # vide la file d'attente série
        except serial.serialutil.SerialException as e:
            popup = Popup(title='System error',
                          content=Label(text="Can't connect to {}: {}".format(
                              self.root.ids.serialport.text,
                              str(e)
                          ))
            )
            popup.open()

    def disconnect(self): # deconnection au port serie
        print("Je me déconnecte du port serie !!")
        self.serial = serial.Serial = None

    def _send_command(self, g_code): # _ et méthode privée utilisée pour l'envoi des commandes alarm, x_move_pos ...
        self.serial.write("{}\r\n\r\n".format(g_code).encode('utf-8'))

    def alarm(self): # Kill alarm lock
        print("Je retire l'alarme")
        self._send_command("$X")

    def rst_xyz(self):  # Reset XYZ
        print("Reset XYZ remise a zero XYZ")
        self._send_command("")

    def x_move_pos(self): # move X+. Il faut remplacer la valeur de X(1) par la valeur du curseur "pas".
        print("mouvement de X en positif")
        self._send_command("G91X1")

    def x_move_neg(self): # move X-
        print("mouvement de X en negatif")
        self._send_command("G91X-1")

    def y_move_pos(self): # move Y+
        print("mouvement de Y en positif")
        self._send_command("G91Y1")

    def y_move_neg(self): # move Y-
        print("mouvement de Y en negatif")
        self._send_command("G91Y-1")

    def z_move_pos(self): # move Z+
        print("mouvement de Z en positif")
        self._send_command("G91Z1")

    def z_move_neg(self): # move Z-
        print("mouvement de Z en negatif")
        self._send_command("G91Z-1")


if __name__ == '__main__':
    windows = ArmApp()
    windows.run()
