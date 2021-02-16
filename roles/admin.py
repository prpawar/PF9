from lib.vm_data_parser import VMDataParser


class Administrator(object):
    # this is singleton class. There could be only one administrator here.
    __instance = None
    __vm_pool = None

    def __new__(class_, *args, **kwargs):
        if not isinstance(class_.__instance, class_):
            class_.__instance = object.__new__(class_, *args, **kwargs)
        return class_.__instance

    def create_vm_pool(self, filepath):
        # Assuming that at given point we only operate on fixed set of VMs.
        if not self.__vm_pool:
            data_parser = VMDataParser(filepath)
            self.__vm_pool = data_parser.get_vm_pool()
        return self.__vm_pool

    def cater_checkout_vm(self, ip):
        # give an access of a vm to some user.
        intended_vm = self.__vm_pool[ip]
        if intended_vm.checkout:
            print("VM with ip {0} is not available at this moment, please try after sometime.".format(ip))
            return -1
        self.__vm_pool[ip].checkout = True
        return (intended_vm.ip, intended_vm.username, intended_vm.password)

    def cater_checkin_vm(self, ip):
        # take an access of a vm from some user.
        self.clear_vm()
        self.__vm_pool[ip].checkout = False
        print("VM with ip {0} is added in pool back".format(ip))

    def clear_vm(self):
        pass

    def monitor_vms(self):
        # check CPU consumption of a vms in pool
        pass 
