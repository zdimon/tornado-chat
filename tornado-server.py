#!/usr/bin/env python
import tornado.ioloop
import tornado.web
loader = tornado.template.Loader(".")
from tornado import autoreload
from tornado.websocket import WebSocketHandler
import json
import datetime
import time
import hashlib


users = [
    {
      'name': 'Dima',
      'uid': 1
    },
    
    {
      'name': 'Vovan',
      'uid': 2
    },
     
]

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", myvar='Hello worlddd', users=users)

class FormHandler(tornado.web.RequestHandler):
    def post(self):
        print(self.get_argument('message'))
        self.render("index.html",  myvar='Hello worlddd', users=users)

ws_clients = {} 

class WebsocketHandler(tornado.websocket.WebSocketHandler):

    def open(self):
        print('Open connection')
        sign = hashlib.md5(str(datetime.datetime.now()).encode('utf-8')).hexdigest()
        self.client_id = sign
        # pass sign to client
        self.write_message(\
            {\
                'action': 'set_sign',\
                'message': sign\
            }\
        )
        #print(sign)
        ws_clients[sign] = self
        #print(ws_clients)
        '''
        while True:
            time.sleep(1)
            self.write_message({'action': 'ping', 'message': str(datetime.datetime.now())})
        '''

    def on_message(self, message):
        print('got message')
        json_message = json.loads(message)
        for c in ws_clients:
            ws_clients[c].write_message({'action': 'onmessage', 'message': json_message['message']})
        

    def on_close(self):
        print('close connection')    
        del ws_clients[self.client_id]

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/submit", FormHandler),
        (r"/websocket", WebsocketHandler),
    ])

if __name__ == "__main__":
    print('Starting server on 8888 port')
    autoreload.start()
    autoreload.watch('.')
    autoreload.watch('index.html')
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()