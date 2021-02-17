Here we are relying on 2 primary classes.

Administrator
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

------------------------------------------------------------------------------

User

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

------------------------------------------------------------------------------

Runner just creates users and start the thread running.
We have used "sudo killall -9 python", to crash the runner. And started over to check if it restores pre-crash state or not.
