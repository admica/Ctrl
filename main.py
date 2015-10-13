#!/usr/bin/env python
__version__ = "1.0"

from kivy.lang import Builder
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock, mainthread
from threading import Thread
import SocketServer
from Queue import Queue

Builder.load_file("kivy.kv")

class RootWidget(FloatLayout):

    def __init__(self, q, **kwargs):
        super(RootWidget, self).__init__(**kwargs)
        self.q = q
        #Clock.schedule_interval(self.q_watch, 0.2)

    def cb_press(self, x):
        print x

    def q_watch(self, *args):
        try:
            data = self.q.get_nowait()
            self.gui_update(data)
        except:
            pass


    def gui_update(self, data):
        # format data
        payload = "Node %s Temp: %s'C RH: %s%% Up: %ss" % (data[0], data[3], data[4], data[5])
        print payload

        # modify gui elements
        if data[0] == '1':
            self.label1.text = payload
        elif data[0] == '2':
            self.label2.text = payload
        elif data[0] == '3':
            self.label3.text = payload
        elif data[0] == '4':
            self.label4.text = payload
        elif data[0] == '5':
            self.label5.text = payload
        elif data[0] == '6':
            self.label5.text = payload
        elif data[0] == '7':
            self.label5.text = payload
        elif data[0] == '8':
            self.label5.text = payload
        elif data[0] == '9':
            self.label5.text = payload
        else:
            print "Invalid data", data


class WebServer(SocketServer.ThreadingTCPServer):

    def __init__(self, options, q):
        self.running = True
        self.options = options
        self.q = q

        # connect to first available port
        port_low, port_high = self.options['port_range']
        for port in range(port_low, port_high):
            try:
                SocketServer.ThreadingTCPServer.__init__(self, ('', port), self.handler)
                break
            except:
                print "Port %s is busy..." % port
        print "Connected on port %s" % port

        self.timeout = 0.5


    def serve_until_stopped(self):
        fd = self.socket.fileno()
        import select
        while self.running:
            try:
                rd, wr, ex = select.select([fd], [], [], self.timeout)
            except Exception as e:
                print "Stopping"
                return False
            if rd:
                self.handle_request()

        # Shutting down
        self.socket.close()
        return False


    def handler(self, socket, tup, obj):
        src, port = tup
        print src,port
        raw = socket.recv(4096)
        raw = raw.split(' ')[1] # get payload element
        data = raw[1:].split('/') # skip leading slash
        print 'handler data:', data

        # queue data
        self.q.put(data)


    def handle_request(self):
        try:
            socket = self.get_request()
            #print socket[0] # <socket._socketobject object at 0x7f6f8b9f6130>
            #print socket[1] # ('127.0.0.1', 36179)
            self.process_request(socket[0], socket[1])
        except Exception as e:
            print "FAILED:", e


class MyApp(App):

    def __init__(self, **kwargs):
        super(MyApp, self).__init__(**kwargs)

        # start with defaults
        self.options = {}
        self.options['port_range'] = (8000,9000)

        # thread shared queue
        self.q = Queue()

        #self.t = Thread(target=self.t_server, args=([self.q,]))
        #self.t.start()


    def t_server(self, q):
        self.webserver = WebServer(self.options, q)
        self.webserver.serve_until_stopped()
        return False


    def on_stop(self):
        """stop python thread before app stops"""
        pass
        #self.webserver.running = False
        

    def build(self):
        return RootWidget(self.q)


if __name__ == "__main__":  
    MyApp().run()

