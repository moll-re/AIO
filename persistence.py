import json
import time

class PersistentVars():
    """"""

    def __init__(self,savefile_path):
        self.path = savefile_path

    def write(self, name, value):
        pre = self.read()
        pre[name] = value
        try:
            file = open(self.path,"w")
            json.dump(pre, file)
            file.close()
        except:
            print("Config not written - critical")

    def read(self, name=""):
        try:
            file = open(self.path,"r")
            vars = json.load(file)
            file.close()
            if len(name) != 0:
                vars = vars[name]
        except:
            vars = None

        return vars
