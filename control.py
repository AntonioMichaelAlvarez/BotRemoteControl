#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
from tornado.web import StaticFileHandler, Application
from tornado.ioloop import IOLoop
from tornado.websocket import WebSocketHandler
import threading
import cv2

video_cap = None
ws_handler = None

class RobotWebSocketHandler(WebSocketHandler):
    clients = []
    def __init__(self, *args, **kwargs):
        global ws_handler
        ws_handler = self
        super(RobotWebSocketHandler, self).__init__(*args, **kwargs)

    def open(self):
        print "WebSocket connection started"
        self.clients.append(self)
        print self.request

    def on_message(self, message):
        # Used to control
        print message

    def on_close(self):
        self.clients.remove(self)

    def put_img(self, imgdata):
        for client in self.clients:
            client.write_message(imgdata, binary=True)


class VideoCap:
    def __init__(self, width=320, height=240):
        # Change this method in order to connect to desired camera device
        # on your target platform
        self.cap = cv2.VideoCapture(0)
        # Set preferred width and height
        self.cap.set(3, width)
        self.cap.set(4, height)
        self.frame = None
        self.is_running = True

    def frame_loop(self):
        global ws_handler
        while self.is_running:
            res, self.frame = self.cap.read()
            cv2.waitKey(1)
            if ws_handler != None:
                # Encode image data to JPEG
                ws_handler.put_img(cv2.imencode(".jpg", self.frame)[1].tostring())

    def stop_acquisition(self):
        self.is_running = False
        self.cap.release()


video_cap = VideoCap()
video_cap_loop = threading.Thread(target=video_cap.frame_loop)
print "Init video_cap_loop"
video_cap_loop.start()
print "Loop started"
try:
    webapp = Application([
        (r"/ws", RobotWebSocketHandler),
        (r"/(?!ws$)(.*)", StaticFileHandler, {
            "path": "./static_www",
            "default_filename": "index.html"
        }),
    ])
    webapp.listen(8080)
    print "Server started"
    IOLoop.current().start()
except KeyboardInterrupt:
    if video_cap_loop is not None:
        video_cap.stop_acquisition()
    print "Stopping polling loop"
