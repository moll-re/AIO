import json
import time
import os
import shutil

class Variables():
    """"""

    def __init__(self, module_name, file_name="persistence/persistent_vars.json", init_name="persistence/persistent_init.json", ):
        self.path = file_name
        self.init_path = init_name

        self.module = module_name

        self.last_action = "" 
        # last performed action, if only reads are made, then the underlying var has not been changed
        # and doesn't need to be read again
        self.savefile = {}

        if not os.path.exists(self.path):
            shutil.copy(self.init_path, self.path)


    def global_action(self, action, name, value=""):
        old = self.module
        self.module = "global"
        action = getattr(self, action)
        if value != "":
            ret = action(name,value)
        else:
            ret = action(name)
        self.module = old
        return ret

    def write(self, name, value):
        pre = self.read("")
        pre[self.module][name] = value
        try:
            file = open(self.path,"w")
            json.dump(pre, file)
            file.close()
            self.last_action = "write"
        except:
            print("Config not written - critical")


    def read(self, name):
        if self.last_action == "read":
            vars = self.savefile
        else:
            file = open(self.path,"r")
            vars = json.load(file)
            file.close()
            self.savefile = vars
            self.last_action = "read"

        if name != "":
            vars = vars[self.module][name]
        return vars


    def increment(self, name, inc=1):
        pre = self.read(name)
        if pre:
    	    self.write(name, pre + inc)
        else:
            self.write(name, inc)
        

    def append_list(self, name, value):
        pre = self.read(name)
        pre.append(value)
        self.write(name, pre)
