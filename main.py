# kivy.require('1.10.0')


from kivy.app import App
from kivy.uix.widget import Widget


import usb_serial


class Desktop(Widget):
    pass
    
class ArmApp(App):

    def build(self):
        return Desktop()

    def idle(self):  # si connecté au port serie, change d'etat le Togglebutton ligne 64 du .kv en 'down'
#        for self.connect() in serial.Serial:
#            self.idle = bool(self.root.ids.idle.state)
#        if self.serial == self.connect():
#            serial.state = 'normal'
#        else:
#            serial.state = 'down'
        pass

    def connect(self):
        usb_serial.connect(self)


    def disconnect(self):  # deconnection au port serie
        print("Je me déconnecte du port serie !!")
        self.serial = usb_serial.Serial = None


    def _send_command(self, g_code):  # _ et méthode privée utilisée pour l'envoi des commandes alarm, x_move_pos ...
        self.serial.write("{}\r\n\r\n".format(g_code).encode('utf-8'))


    def alarm(self):  # Kill alarm lock
        print("Je retire l'alarme")
        self._send_command("$X")


    def rst_grbl(self):  # Reset GRBL
        print("Je retire reset GRBL")
        self._send_command("ctrl-x")


    def cycle_start(self):  # demarre cycle à voir si c'est utile
        print("Je demarre un cycle")
        self._send_command("~")


    def feed_hold(self):
        print("Feed_hold ??")
        self._send_command("!")


    def rst_xyz(self):  # Reset XYZ
        print("Reset XYZ remise a zero XYZ")
        self._send_command("G92X0Y0Z0")  # commande gcode a revoir


    def rst_x(self):  # Reset X
        print("Reset X remise a zero X")
        self._send_command("G10P0L20X0")  # commande gcode a revoir


    def rst_y(self):  # Reset X
        print("Reset Y remise a zero Y")
        self._send_command("G92Y0")  # commande gcode a revoir


    def rst_z(self):  # Reset Z
        print("Reset Z remise a zero Z")
        self._send_command("G92Z0")  # commande gcode a revoir


    def home(self):  # Retour X0 Y0 Z0
        print("Retour position X0Y0Z0")
        self._send_command("G30")


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

    def serial_list(self):
        ports = usb_serial.serial_list()
        print("port list: {}".format(",".join(ports)))    
        return ports


if __name__ == '__main__':
    ArmApp().run()
