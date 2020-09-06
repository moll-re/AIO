import json
import time
import os
class Variables():
    """"""

    def __init__(self, savefile_path, init_path):
        self.path = savefile_path
        self.init_path = init_path
        self.last_action = ""
        # last performed action, if only reads are made, then the underlying var has not been changed
        # and doesn't need to be read again
        self.savefile = {}

    def write(self, name, value):
        pre = self.read()
        pre[name] = value
        try:
            file = open(self.path,"w")
            json.dump(pre, file)
            file.close()
            self.last_action = "write"
        except:
            print("Config not written - critical")


    def read(self, name=""):
        if self.last_action == "read":
            if name == "":
                return self.savefile
            else:
                return self.savefile[name]

        try:
            if os.path.exists(self.path):
                file_path = self.path
            else:
                file_path = self.init_path
            file = open(file_path,"r")
            vars = json.load(file)
            file.close()
            self.savefile = vars
            self.last_action = "read"
        except:
            return None

        if name != "":
            vars = vars[name]
        return vars


    def increment(self, name=""):
        pre = self.read(name)
        plus1 = pre + 1
        self.write(name, plus1)
