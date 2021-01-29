import json
import os



class PersistentDict(dict):
    """Extended dict that writes its content to a file every time a value is changed"""

    def __init__(self, file_name, *args, **kwargs):
        """initialization of the dict and of the required files"""
        super().__init__(*args, **kwargs)

        self.path = file_name
        self.last_action = ""
        if not os.path.exists(self.path):
            with open(self.path, "a") as f:
                f.write("{}")
        self.read_dict()

    ## helper - functions
    def write_dict(self):
        with open(self.path, "w") as f:
            json.dump(self, f)
        self.last_action = "w"

    def read_dict(self):
        with open(self.path) as f:
            tmp = dict(json.load(f))
            for key in tmp:
                super().__setitem__(key, tmp[key])
        self.last_action = "r"

    ## extended dictionary - logic
    def __setitem__(self, key, value):
        if self.last_action != "r":
            self.read_dict()
        # not sure if the step to read is necessary, but I'll keep it for safety
        super().__setitem__(key,value)
        self.write_dict() # writes 'self' to a json file.

    def __getitem__(self, key):
        if self.last_action != "r":
            self.read_dict()
        
        ret_val = super().__getitem__(key)
        if type(ret_val) == dict:
            ret_val = HookedDict(key, self, ret_val)

        return ret_val
    
    def clear(self):
        super().clear()
        self.write_dict()
        return {}



class HookedDict(dict):
    """helper class to detect writes to a child-dictionary and triger a write in PersistentDict"""

    def __init__(self, own_name, parent_dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = own_name
        self.parent = parent_dict
    
    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.parent.__setitem__(self.name, self)

    def __getitem__(self, key):
        ret_val = super().__getitem__(key)
        if type(ret_val) == dict:
            ret_val = HookedDict(key, self, ret_val)
        return ret_val
    
    def pop(self, k, d=None):
        retvalue = super().pop(k, d)
        self.parent.__setitem__(self.name, self)
        return retvalue
