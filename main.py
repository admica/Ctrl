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
    port = 8000

    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)


    def cb_label_host_text(self, *args):
        # dont allow some chars
        if args[0][-1] in [ '\r', '\n', '   ', ' ' ]:
            self.ids.input_host.text = args[0][:-1]
        else:
            # set host
            self.host = args[0]

    def cb_label_port_text(self, *args):
        # only allow digits
        try:
            int(args[0][-1])
            # set port
            self.port = int(args[0])
        except ValueError:
            self.ids.input_port.text = args[0][:-1]



    def cb_button_connect_press(self, *args):
        # set connecting label
        self.ids.label_connecting.text = "Connecting to %s:%s" % (self.host, self.port)

        # go to connecting screen
        self.ids.screenmgr.current = "screen_connecting"

        # start client thread
        self.t = Thread(target=self.t_client, args=())
        self.t.start()


    def t_client(self):
        try:
            print "Connecting...", self.host, self.port
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.settimeout(5)
            self.s.connect((self.host, self.port))

            Clock.schedule_once(self.conn_yes, 0)

            # stop thread
            return False

        except Exception as e:
            # failed to connect
            del self.s

            Clock.schedule_once(self.conn_no, 0)

        # stop thread
        return False


    def conn_no(self, *args):
        # change setup heading
        self.ids.label_heading.text = "Failed to connect. Try again?"

        # change back to setup screen
        self.ids.screenmgr.current = "screen_setup"


    def conn_yes(self, *args):
        # connected, go to main screen
        self.ids.screenmgr.current = "screen_main"


    def cb_press(self, keys):
        """user pushed button on the ctrl panel"""
        print keys
        try:
            self.s.send(keys)
        except Exception as e:
            print "Error <%s> trying to send [%s]" % (e, keys)


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

