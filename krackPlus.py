#!/bin/python

#NOTES:
## Sultan is one way to run bash commands simply: https://github.com/aeroxis/sultan

# Kivy framework is used for GUI
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label 
from kivy.core.window import Window

# Subprocess is used to run bash commands
import subprocess

# Setup: installs necessary software and sets up a test network 
class ClientScanSetup(Widget):
	pass
	#Should use subprocess to run a bash script

# Defines the instance of the widget.
class KrackWidget(Widget):
	pass # used to keep a class valid even though it doesn't contain anything

class KrackPlusApp(App):
	def build(self):
		Window.size = (820, 580)	
		#TODO should be a nice gray or something
		Window.clearcolor = (.12,.12,.12,.12)
		exampleLabel=Label(text='Welcome to KRACK+')
		return exampleLabel

if __name__ == '__main__':
	KrackPlusApp().run()
