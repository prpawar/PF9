import os

from roles.admin import Administrator
from roles.user import User

threads = []
no_of_users = 4
available_ips = [
    "172.19.0.1",
    "172.17.0.1",
    "172.21.0.1",
    "172.17.0.1",
]

# Create new threads
for ele in range(no_of_users):
    threads.append(
        User(**{
            "name": "UserThread-{0}".format(ele),
            "machine_ip": available_ips[ele]
        })
    )

# Start new Threads
[user.start() for user in threads]

# Wait for all threads to complete
for t in threads:
    t.join()


print("Exiting Main Thread")
os.system("rm -rf data/.tmp.json")
