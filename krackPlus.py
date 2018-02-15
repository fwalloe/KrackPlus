#!/bin/python

# Kivy framework is used for GUI
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label 


# Defines the instance of the widget.
class KrackWidget(Widget):
	pass # pass is used to keep the class valid but allow it not to contain anything 

class KrackPlusApp(App):
	def build(self):
		exampleLabel=Label(text='Welcome to KRACK+')
		return exampleLabel


if __name__ == '__main__':
	KrackPlusApp().run()
