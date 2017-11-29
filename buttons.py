# buttons.py

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
