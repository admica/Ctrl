#!/usr/bin/env python
__version__ = "1.0"

from kivy.lang import Builder
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock, mainthread
from threading import Thread
import socket

Builder.load_file("kivy.kv")

class RootWidget(FloatLayout):

    host = '192.168.1.100'
    port = 2000

    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(5)

        self.t = Thread(target=self.t_client, args=())
        self.t.start()

    def cb_label_host_text(self, *args):
        print args

    def cb_label_host_port(self, *args):
        print args

    def cb_press(self, keys):
        print keys
        try:
            self.s.send(keys)
        except Exception as e:
            print "Error <%s> trying to send [%s]" % (e, keys)


    def t_client(self):
        try:
            print "Connecting..."
            self.s.connect((self.host, self.port))

            # connected
            print "Connected"

        except Exception as e:
            print "Error <%s> connecting to %s:%s" % (e, self.host, self.port)

        # stop thread
        return False


class MyApp(App):

    def __init__(self, **kwargs):
        super(MyApp, self).__init__(**kwargs)

        # start with defaults
        self.options = {}
        self.options['port_range'] = (1025,65535)


    def on_stop(self):
        """stop python thread before app stops"""
        self.running = False
        

    def build(self):
        return RootWidget()

if __name__ == "__main__":  
    MyApp().run()

