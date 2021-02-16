import os
import json
from lib.vm_factory import VMFactory

class VMDataParser(object):
    def __init__(self, filepath):
        self.filepath = filepath
        assert os.path.exists(self.filepath), "Given file does not exists"
        # parsing this in init method to avoid repetative reads.
        with open(self.filepath, "r") as fp:
            self.vm_details = json.load(fp)

    def get_vm_pool(self):
        result = {}
        for vm_details in self.vm_details.get("vms"):
            result[vm_details["ip"]] = VMFactory(**vm_details)
        return result

