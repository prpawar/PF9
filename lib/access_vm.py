import paramiko

class AccessVM(object):
    """
    This class defines methods to ssh to vm and run given commands
    """
    def __init__(self, *args, **kwargs):
        self.ip = kwargs.get("ip")
        self.username = kwargs.get("username")
        self.password = kwargs.get("password")
        self.get_vm_connection()

    def get_vm_connection(self):
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(
            hostname=self.ip,
            username=self.username,
            password=self.password
        )
        self.ssh_client = ssh_client

    def execute_ssh_command(self, command):
        # returns stdin, stdout, stderr
        return self.ssh_client.exec_command(command)

    """
    @staticmethod
    def copy_file(ssh_client, source_path, dest_path):
        return ssh.open_sftp().put(source_path, dest_path)
    """

    def cleanup_vm(self):
        # returns stdin, stdout, stderr
        return self.ssh_client.exec_command("rm -rf /tmp/*")
