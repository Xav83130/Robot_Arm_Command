# kivy.require('1.10.0')


from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.logger import Logger

import serial
import serial.serialutil
import serial.tools.list_ports
import pprint
import time

# import usb_serial


class Desktop(Widget):
    pass


class ArmApp(App):
    def __init__(self):
        # Un constructeur (__init__) est appele au moment de la creation d'une instance de classe (Donc l'objet)
        # Cette methode permet de creer des variables de classe
        self.serial = None
        # Position initiales des axes
        self.axe_x = 0
        self.axe_y = 0
        self.axe_z = 0
        # La ligne d'en desous permet d'appeler le constructeur de la classe App, important !
        super().__init__()

    def build(self):
        return Desktop()

    def view_connect(self):  # si connecté au port serie, change d'etat le Togglebutton ligne 64 du .kv en 'down'
        if self.serial is not None and self.serial.is_open:
            self.root.ids.viewconnect.state = 'down'
        else:
            self.root.ids.viewconnect.state = 'normal'

    def get_line(self):
        data = self.serial.readline()
        return data.decode("utf-8")

    def get_lines(self):
        lines = []
        while self.serial.inWaiting() > 0:
            line = self.get_line()
            lines.append(line)
        pprint.pprint(lines)
        return lines

    def connect(self):

        Logger.info("Connecting to serial device: {} with baudrate: {}".format(
            self.root.ids.serialport.text,
            self.root.ids.baudrate.text))
        # int() est nécessaire car la valeur renvoyé par .text est une str, et le type attendu est un int
        try:
            self.serial = serial.Serial(self.root.ids.serialport.text,
                                        int(self.root.ids.baudrate.text))
            self.view_connect()
            while True:
                line = self.get_line()
                pprint.pprint(line)
                if line == "['$H'|'$X' to unlock]\r\n":
                    break
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

    def disconnect(self):  # deconnection au port serie
        print("Je me déconnecte du port serie !!")
        self.serial.close()
        self.serial = None
        self.view_connect()

    def serial_list(self):
        serial_ports = []
        for p in serial.tools.list_ports.comports():
            serial_ports.append(p[0])
        return serial_ports

    def view_input(self): # prévue pour visualiser les infos retourné par grbl dans 'codeinput' ligne 259 du .kv
        lines = self.get_lines()
        self.root.ids.cmd_results.text = ", ".join(lines)

    def idle(self):
        input = "<Idle|MPos:0.000,0.000,0.000|FS:0.0,0>"               # la commande '?' me renvoi : '<Alarm,MPos:0.000,0.000,0.000,WPos:0.000,0.000,0.000>\r\n'
        (_, axes, _) = input.strip("<>").split("|")                    # ou '<Idle,MPos:0.000,0.000,0.000,WPos:0.000,0.000,0.000>\r\n' Alarm ou Idle
        (x, y, z) = [float(_) for _ in axes.split(":")[1].split(",")]  # Mpos = Machine position listed as X,Y,Z coordinates Wpos = Work position listed as X,Y,Z coordinates

    def _send_command(self, g_code):  # _ et méthode privée utilisée pour l'envoi des commandes alarm, x_move_pos ...
        print("g_code: {}".format(g_code))
        self.serial.write("{}\n".format(g_code).encode('utf-8'))
        while True:
            line = self.get_line()
            pprint.pprint(line)
            if line == 'ok\r\n':
                break
        return line

    def alarm(self):  # Kill alarm lock
        print("Je retire l'alarme")
        self._send_command("$X")    # commande OK

    def rst_grbl(self):  # Reset GRBL
        print("Reset GRBL")
        self._send_command("0x18")  # ERREUR 'error: Expected command letter\r\n'

    def cycle_start(self):  # demarre cycle à voir si c'est utile
        print("Reprise")
        self._send_command("~")

    def feed_hold(self):
        print("Pause")
        self._send_command("!")

    def rst_xyz(self):  # Reset XYZ
        print("Reset XYZ remise a zero XYZ")
        self._send_command("G30.1")  # commande OK

    def rst_x(self):  # Reset X
        print("Reset X remise a zero X")
        self._send_command("G92 X0")  # commande gcode a revoir

    def rst_y(self):  # Reset X
        print("Reset Y remise a zero Y")
        self._send_command("G92 Y0")  # commande gcode a revoir

    def rst_z(self):  # Reset Z
        print("Reset Z remise a zero Z")
        self._send_command("G92 Z0")  # commande gcode a revoir

    def home(self):  # Retour X0 Y0 Z0
        print("Retour position X0Y0Z0")
        self._send_command("G30")    # commande OK

    def x_move_pos(self):  # move X+. Il faut remplacer la valeur de X(1) par la valeur du curseur "pas".
        print("mouvement de X en positif")
        self._send_command("G91X1")

    def x_move_neg(self):  # move X-
        print("mouvement de X en negatif")
        self._send_command("G91X-1")

    def y_move_pos(self):  # move Y+
        print("mouvement de Y en positif")
        self._send_command("G91Y1")

    def y_move_neg(self):  # move Y-
        print("mouvement de Y en negatif")
        self._send_command("G91Y-1")

    def z_move_pos(self):  # move Z+
        print("mouvement de Z en positif")
        self._send_command("G91Z1")

    def z_move_neg(self):  # move Z-
        print("mouvement de Z en negatif")
        self._send_command("G91Z-1")

    def infos(self):
        self._send_command('$$')  # commande OK



if __name__ == '__main__':
    ArmApp().run()
