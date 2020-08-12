import json
import time

class Variables():
    """"""

    def __init__(self,savefile_path):
        self.path = savefile_path
        self.last_action = ""
        # last performed action, if only reads are made, then the underlying var has not been changed
        # and doesn't need to be read again
        self.savefile = {}

    def write(self, name, value):
        if self.last_action == "read":
            pre = self.savefile
        else:
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
            vars = self.savefile
        else:
            try:
                file = open(self.path,"r")
                vars = json.load(file)
                file.close()
                self.savefile = vars
                self.last_action = "read"
            except:
                return None

        if len(name) != 0:
            vars = vars[name]

        return vars

    def increment(self, name=""):
        if self.last_action == "read":
            pre = self.savefile
        else:
            pre = self.read()

        try:
            pre[name] += 1
            file = open(self.path,"w")
            json.dump(pre, file)
            file.close()
            self.last_action = "write"
        except:
            print("Config not written - critical")
