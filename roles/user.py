import time
import threading

from lib.access_vm import AccessVM
from roles.admin import Administrator


class User(threading.Thread):
    """
    This class is a threading class, so we can have n numbers of users running at the same time.
    Actions performed:
        1. While object creation, user registers with vm on which it wants to work.
            eg. [UserThread-0]: Wants to monitor 172.19.0.1
                [UserThread-1]: Wants to monitor 172.21.0.1

        2. Beore checkout a vm, user will checkin vm if he already didnt. (maybe program has crashed earlier.)
            eg. [UserThread-1]: Checkout VM with IP 172.19.0.1
                [ADMIN]: VM with ip 172.19.0.1 is not available at this moment, please try after sometime.
                [UserThread-1]: Seems like I am holding VM 172.19.0.1, checkin this VM
                [UserThread-1]: Checkin VM with IP 172.19.0.1

        3. User checkout vm, waits for some time if machine is busy and retries
            eg. [UserThread-5]: Checkout VM with IP 172.21.0.1
                [ADMIN]: VM with ip 172.21.0.1 is not available at this moment, please try after sometime.
                <user sleeps here>
                [UserThread-5]: Retrying
                [UserThread-5]: Checkout VM with IP 172.21.0.1

        4. When user gets VM, he accesses vm to get its `vmstats` and print it
            eg. [UserThread-3]: Memory Utilisation of 172.21.0.1 is ['      4000.........]

        5. After work is done, user checkins vm to administrator, to add back in pool
            eg. [UserThread-2]: Done working
                [UserThread-2]: Checkin VM
                [ADMIN]: VM with IP 172.19.0.1 is cleaned up
                [ADMIN]: VM with ip 172.19.0.1 is added in pool back
                [UserThread-2]: Finished

        6. Its possible that user might not get vm to use in its time limit.
            eg. [UserThread-3]: Retrying
                [UserThread-3]: Checkout VM
                [ADMIN]: VM with ip 172.19.0.1 is not available at this moment, please try after sometime.
                [UserThread-3]: Could not get machine to work in time limit, Finished

    """
    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self)
        self.name = kwargs.get("name")
        self.machine_ip = kwargs.get("machine_ip")
        self.work_done = False
        self.admin = Administrator()
        print(f"[{self.name}]: Wants to monitor {self.machine_ip}")

    def checkout_vm(self):
        print(f"[{self.name}]: Checkout VM")
        return self.admin.cater_checkout_vm(self.machine_ip, self)

    def checkin_vm(self):
        print(f"[{self.name}]: Checkin VM")
        return self.admin.cater_checkin_vm(self.machine_ip)
 
    def work(self, client):
        print(f"[{self.name}]: Started working")
        # adding some delay, so other users can wait
        time.sleep(2)
        stdin, stdout, stderr = client.execute_ssh_command("vmstat -s")
        print(f"[{self.name}]: Memory Utilisation of {self.machine_ip} is {stdout.readlines()}")
        print(f"[{self.name}]: Done working")

    def run(self):
        retry_count = 10
        for count in range(retry_count):
            result = self.checkout_vm()
            if not result.get("success"):
                if result.get("checkout") == self.name:
                    print(f"[{self.name}]: Seems like I am holding VM {self.machine_ip}, checkin this VM")
                    self.checkin_vm()
                    continue
                # else someone else is using this machine.
                time.sleep(5)
                print(f"[{self.name}]: Retrying after 10 secs")
                continue

            # else "success": True
            break

        if result.get("success"):
            client = AccessVM(**result)
            self.work(client)
            self.checkin_vm()
            self.work_done = True
            print(f"[{self.name}]: Finished")
        else:
            print(f"[{self.name}]: Could not get machine to work in time limit, Finished")
