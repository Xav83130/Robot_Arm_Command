# kivy.require('1.10.0')

import serial
import time
import multiprocessing

import kivy

from kivy.app import App
from kivy.uix.widget import Widget
#from kivy.uix.boxlayout import BoxLayout
#from kivy.uix.textinput import TextInput
#from kivy.uix.image import Image
from kivy.properties import ObjectProperty

# definition du port serie et du baudrate
SERIAL_PORT = '/dev/tty.wchusbserialfd130'
SERIAL_BAUDRATE = 115200


class Desktop(Widget):
    pass


class ArmApp(App):


    def build(self):
        return Desktop()

    def viewport(self): # Le port serie entré dans le textinput est utilisé pour la connection serie
        pass

    def baudrate(self): # Utilise le baudrate du textinput ligne 39 du .kv pour se connecter
        pass

    def idle(self): # change d'etat le Togglebutton ligne 64 du .kv
        # si je suis connecté au port serie
        # alors le bouton change d'etat 'state: down'
        pass

    def connect(self): # connection au port serie
        print("Je me connecte au port serie !!")
        self.serial = serial.Serial(SERIAL_PORT, SERIAL_BAUDRATE)
        time.sleep(2)  # Attend que GRBL s'initialise
        self.serial.flushInput()  # vide la file d'attente série

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


windows = ArmApp()
windows.run()
