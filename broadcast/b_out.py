import flask
from flask import request, jsonify
import numpy as np
from threading import Thread


class BroadcastUpdates:
    """Broadcasts (out) updates for the hw-handler to be fetched periodically"""
    
    def __init__(self, port):
        """"""
        self.last_show = ""

        self.queue = [] #[{"matrices" : [np.full((16,16,3), 10).tolist(), np.full((16,16,3), 100).tolist(), np.full((16,16,3), 200).tolist()]} for _ in range(4)]
        self.port = port


    def start(self):
        t = Thread(target=self.run)
        t.start()


    def run(self):
        app = flask.Flask(__name__)
        
        @app.route('/getupdates', methods=['GET'])
        def get_updates():
            return self.get_updates()
        @app.route('/getlast', methods=['GET'])
        def get_last():
            return self.get_last()
        
        app.run('0.0.0.0', port=self.port)
    
    
    def get_updates(self):
        try:
            data = self.queue.pop(0)
            self.last_show = data
            is_new = True
            has_queue = len(self.queue) > 0
        except:
            data = ""
            is_new = False
            has_queue = False
        
        return self.generate_response(
            is_new = is_new,
            data = data,
            has_queue = has_queue
        )



    def get_last(self):
        try:
            try:
                data = self.queue[-1]
                self.queue = []
            except: # list empty
               data = self.last_show,
        except:
            data = ""
        return self.generate_response(
            data = data,
            has_queue = False,
        )



    def generate_response(self, **kwargs):
        ret = {
            "status" : "ok",
            **kwargs
        }
        print(ret)
        return jsonify(ret)

