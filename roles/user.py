class User(object):
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get(name)

    def checkout_vm(self):
        # ask for access of a vm
        pass
    
    def checkin_vm(self):
        # give away its access when work is done.
        pass
    
    def work(self):
        print("Working on a VM")

