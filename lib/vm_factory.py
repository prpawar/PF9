
class VMFactory(object):
    # not exactly factory class though
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get("name")
        self.ip = kwargs.get("ip")
        self.os = kwargs.get("os")
        self.username = kwargs.get("username")
        self.password = kwargs.get("password")
        self.checkout = False
        self.clear = True
