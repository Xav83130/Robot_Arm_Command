#kivy.require('1.10.0')

import kivy

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.graphics import Line

class Desktop(Widget):
    pass

class ArmApp(App):
    def build(self):
        return Desktop()

windows = ArmApp()
windows.run()