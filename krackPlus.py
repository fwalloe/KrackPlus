#!/bin/python

#Kivy framework is used for GUI
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button


class KrackWidget(Widget):
	pass

class KrackPlusApp(App):
    def build(self):
        return KrackWidget()


if __name__ == '__main__':
	KrackPlusApp().run()
