# kivy.require('1.10.0')


from kivy.app import App
from kivy.clock import Clock
from kivy.logger import Logger
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput

import serial
import serial.serialutil
import serial.tools.list_ports
import pprint
import time


# import usb_serial

def values_cleanup(string):
    # string = "MPos:0.000,0.000,0.000"
    # returns [ "MPos", [ 0.0, 0.0, 0.0 ] ]
    (name, value_string) = string.split(":")
    values = value_string.split(",")
    return [name, [float(x) for x in values]]


def response_cleanup(string):
    # string = "<Idle|MPos:0.000,0.000,0.000|FS:0,0|WCO:0.000,0.000,0.000>"
    # returns { "state": "Idle", "MPos": [ 0.0, 0.0, 0.0 ], "FS": [ 0.0, 0.0 ], "WCO": [ 0.0, 0.0, 0.0 ] }
    elements = string.strip("<>\r\n").split("|")
    iterator = iter(elements)
    result = {"state": next(iterator)}
    for element in iterator:
        (name, values) = values_cleanup(element)
        result[name] = values
    return result


class Desktop(Widget):
    pass


class ArmApp(App):
    def __init__(self):
        # Un constructeur (__init__) est appele au moment de la creation d'une instance de classe (Donc l'objet)
        # Cette methode permet de creer des variables de classe
        self.serial = None
        # Position initiales des axes
        self.wp_axe_x = 0.00
        self.wp_axe_y = 0.00
        self.wp_axe_z = 0.00
        self.mp_axe_x = 0.00
        self.mp_axe_y = 0.00
        self.mp_axe_z = 0.00
        # La ligne d'en desous permet d'appeler le constructeur de la classe App, important !
        super().__init__()

    def build(self):
        Clock.schedule_interval(self.position_timer, 0.07)
        return Desktop()

    def is_connected(self):
        return self.serial is not None and self.serial.is_open

    def update_view_connect(self):  # si connecté au port serie, change d'etat le Togglebutton ligne 64 du .kv en 'down'
        if self.is_connected():
            self.root.ids.viewconnect.state = 'down'
        else:
            self.root.ids.viewconnect.state = 'normal'

    def get_line(self):
        data = self.serial.readline()
        pprint.pprint(data)
        return data.decode("utf-8")

    def get_lines(self):
        lines = []
        while self.serial.inWaiting() > 0:
            line = self.get_line()
            lines.append(line)
            self.root.ids.cmd_results.text += lines

        return lines

    def connect(self):

        Logger.info("Connecting to serial device: {} with baudrate: {}".format(
            self.root.ids.serialport.text,
            self.root.ids.baudrate.text))
        # int() est nécessaire car la valeur renvoyé par .text est une str, et le type attendu est un int
        try:
            self.serial = serial.Serial(self.root.ids.serialport.text,
                                        int(self.root.ids.baudrate.text))
            self.update_view_connect()
            while True:
                line = self.get_line()
                self.root.ids.cmd_results.text += line
                if line.startswith("Grbl ") and line.endswith(" ['$' for help]\r\n"):
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
        self.update_view_connect()

    def serial_list(self):
        serial_ports = []
        for p in serial.tools.list_ports.comports():
            serial_ports.append(p[0])
        return serial_ports

    def position_timer(self, delta):
        if not self.is_connected():
            return
        result = self._send_command("?")
        if len(result) != 1:
            return
        # GRBL1.1f:result[0]: <Idle|MPos:0.000,0.000,0.000|FS:0,0|WCO:0.000,0.000,0.000>
        response = response_cleanup(result[0])

        mpos_details = response["MPos"]
        self.mp_axe_x = mpos_details[0]
        self.mp_axe_y = mpos_details[1]
        self.mp_axe_z = mpos_details[2]
        self.root.ids.mpos_x.text = str(mpos_details[0])
        self.root.ids.mpos_y.text = str(mpos_details[1])
        self.root.ids.mpos_z.text = str(mpos_details[2])

        if "WCO" in response:
            wco_details = response["WCO"]
            # wpos_details = [ 0.0, 0.0, 0.0 ]
            self.wp_axe_x = wco_details[0]
            self.wp_axe_y = wco_details[1]
            self.wp_axe_z = wco_details[2]
            self.root.ids.wpos_x.text = str((mpos_details[0]) - (wco_details[0]))
            self.root.ids.wpos_y.text = str((mpos_details[1]) - (wco_details[1]))
            self.root.ids.wpos_z.text = str((mpos_details[2]) - (wco_details[2]))

#            pprint.pprint((self.wp_axe_x, self.wp_axe_y, self.wp_axe_z, self.mp_axe_x, self.mp_axe_y, self.mp_axe_z))
    def _send_command(self, g_code):  # _ et méthode privée utilisée pour l'envoi des commandes alarm, x_move_pos ...
#        print("g_code: {}".format(g_code))
        self.serial.write("{}\r\n".format(g_code).encode('utf-8'))
        self.serial.flushInput()
        lines = []
        while True:
            line = self.get_line()
            if line == 'ok\r\n':
                break
            lines.append(line)
        return lines

    def alarm(self):  # Kill alarm lock
        a = self._send_command('$X')  # commande OK
        self.root.ids.cmd_results.text += str(a)

    def parser_state(self):  # parser state
        a = self._send_command('$G')  # commande OK
        self.root.ids.cmd_results.text += str(a)

    def infos(self):
        all_lines = self._send_command('$$')  # commande OK
        for line in all_lines:
            self.root.ids.cmd_results.text += line

    def cycle_start(self):  # commande OK
        self.root.ids.cmd_results.text += "Cycle Strat ~\n"
        self._send_command("~")

    def feed_hold(self):  # commande OK
        self.root.ids.cmd_results.text += "Feed Hold !\n"
        self._send_command("!")

    def rst_xyz(self):  # Reset XYZ
        self.root.ids.cmd_results.text += "Reset G92X0Y0Z0\n"
        self._send_command("G92X0Y0Z0")     # commande OK

    def rst_x(self):  # Reset X
        self.root.ids.cmd_results.text += "Reset X0\n"
        self._send_command("G92 X0")        # commande OK

    def rst_y(self):  # Reset X
        self.root.ids.cmd_results.text += "Reset Y0\n"
        self._send_command("G92 Y0")        # commande OK

    def rst_z(self):  # Reset Z
        self.root.ids.cmd_results.text += "Reset Z0\n"
        self._send_command("G92 Z0")        # commande OK

    def home(self):  # Retour X0 Y0 Z0
        self.root.ids.cmd_results.text += "Home\n"
        self._send_command("G90X0Y0Z0")     # commande OK

    def x_move_pos(self):                   # commande OK
#        print("mouvement de X en positif")
        self._send_command("G91X%s" % str(self.root.ids.curseur_pas.value))

    def x_move_neg(self):  # move X-
#        print("mouvement de X en negatif")
        self._send_command("G91X-%s" % str(self.root.ids.curseur_pas.value))

    def y_move_pos(self):  # move Y+
#        print("mouvement de Y en positif")
        self._send_command("G91Y%s" % str(self.root.ids.curseur_pas.value))

    def y_move_neg(self):  # move Y-
#        print("mouvement de Y en negatif")
        self._send_command("G91Y-%s" % str(self.root.ids.curseur_pas.value))

    def z_move_pos(self):  # move Z+
#        print("mouvement de Z en positif")
        self._send_command("G91Z%s" % str(self.root.ids.curseur_pas.value))

    def z_move_neg(self):  # move Z-
#        print("mouvement de Z en negatif")
        self._send_command("G91Z-%s" % str(self.root.ids.curseur_pas.value))

    def save(self, cmd_send_list):
        gcode_export = open('Gcode.arm', 'w')
        gcode_export.write(str(cmd_send_list))
        gcode_export.close()
        box = BoxLayout()
        box.add_widget(Label(text='Export OK'))

        popup = Popup(title='Export G-code',
                      content=box,
                      size_hint=(None, None),
                      size=(400, 100))
        popup.open()

    def save_pos(self, delta=None):
        self.position_timer(delta)
        self.root.ids.cmd_send_list.text += "G01X{}Y{}Z{}F{}\n".format(
            str(self.root.ids.mpos_x.text),
            str(self.root.ids.mpos_y.text),
            str(self.root.ids.mpos_z.text),
            str(self.root.ids.curseur_vitesse.value)
        )

    def help(self):
        box = BoxLayout()
        box.add_widget(Label(text='Kill alarm     = $X\n'
                                  'Reset XYZ   = Workposition X0 Y0 Z0\n'
                                  'Reset X       = Workposition X0\n'
                                  'Reset Y       = Workposition Y0\n'
                                  'Reset Z       = Workposition Z0\n'
                                  'Home          = Goto Workposition X0 Y0 Z0\n'
                                  'Feed Hold    = Pause !\n'
                                  'Cycle Start   = Restart cycle ~\n'
                                  'State            = Parser State $G\n'
                                  'Setting          = view GRBL setting $$\n'
                                  'Save Position    = Save Arm position\n'
                                  'Start               = Start all positions\n'
                             ))
        popup = Popup(title='Help',
                      content=box,
                      size_hint=(None, None),
                      size=(600, 500))
        popup.open()


if __name__ == '__main__':
    ArmApp().run()