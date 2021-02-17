import os
import pickle

from lib.access_vm import AccessVM
from lib.vm_data_parser import VMDataParser
from lib.constants import DATAFILE, DUMPFILE

class Administrator(object):
    # this is singleton class. There could be only one administrator here.
    """
    Administer is a singleton object, there could be only admin present.
    Actions performed:
        1. While object creation, admin restores previous state if it finds a backup dump file(data/.tmp.json)
            eg. [ADMIN]: Seems like admin crashed earlier, restoring vm pool

        2. Otherwise admin will parse vm details from data file and add vms into pool

        3. When user requests for vm, admin marks vm.checkout with username (easy to track)
           And returns ssh details to user.
            eg. [UserThread-0]: Checkout VM
                [ADMIN]: VM with IP 172.19.0.1 is checked out by UserThread-0
                [UserThread-4]: Checkout VM
                [ADMIN]: VM with IP 172.17.0.1 is checked out by UserThread-4

        4. If requested vm is not available, then ask user to wait.
            eg. [ADMIN]: VM with ip 172.19.0.1 is not available at this moment, please try after sometime.

        5. When user checkin a vm, perform cleanup + remove user.name from vm.checkout parameter, and move ahead.
            eg. [UserThread-2]: Checkin VM
                [ADMIN]: VM with IP 172.19.0.1 is cleaned up
                [ADMIN]: VM with ip 172.19.0.1 is added in pool back
    """
    __instance = None

    def __new__(class_, *args, **kwargs):
        if not isinstance(class_.__instance, class_):
            class_.__instance = object.__new__(class_, *args, **kwargs)
            if os.path.exists(DUMPFILE):
                print(f"[ADMIN]: Seems like admin crashed earlier, restoring vm pool")
                class_.__instance._vm_pool = pickle.load(open(DUMPFILE, "rb"))
            else:
                class_.__instance._vm_pool = VMDataParser(DATAFILE).get_vm_pool()
        return class_.__instance

    def dump_current_pool(self):
        return pickle.dump(self._vm_pool, open(DUMPFILE, "wb"))

    def cater_checkout_vm(self, ip, user):
        intended_vm = self._vm_pool[ip]
        if intended_vm.checkout:
            print(f"[ADMIN]: VM with ip {ip} is not available at this moment, please try after sometime.")
            return {
                "success": False,
                "checkout": intended_vm.checkout,
            }

        self._vm_pool[ip].checkout = user.name
        self.dump_current_pool()
        print(f"[ADMIN]: VM with IP {ip} is checked out by {user.name}")
        return {
            "success": True,
            "ip": intended_vm.ip,
            "username": intended_vm.username,
            "password": intended_vm.password,
        }

    def cater_checkin_vm(self, ip):
        # take an access of a vm from some user.
        intended_vm = self._vm_pool[ip]
        client = AccessVM(**{
            "ip": intended_vm.ip,
            "username": intended_vm.username,
            "password": intended_vm.password,
        })
        client.cleanup_vm()
        self.dump_current_pool()
        print(f"[ADMIN]: VM with IP {ip} is cleaned up")
        self._vm_pool[ip].checkout = None
        print(f"[ADMIN]: VM with ip {ip} is added in pool back")

