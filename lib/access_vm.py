import paramiko

class AccessVM(object):
    def __init__(self, *args, **kwargs):
        self.ip = kwargs.get("ip")
        self.username = kwargs.get("username")
        self.password = kwargs.get("password")

    def get_vm_connection(self):
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(
            hostname=self.ip,
            username=self.username,
            password=self.password
        )
        return ssh_client

    @staticmethod
    def execute_ssh_command(ssh_client, command):
        # returns stdin, stdout, stderr
        return ssh_client.exec_command(command)

    """
    @staticmethod
    def copy_file(ssh_client, source_path, dest_path):
        return ssh.open_sftp().put(source_path, dest_path)
    """

    @staticmethod
    def cleanup_vm(ssh_client):
        # returns stdin, stdout, stderr
        return ssh_client.execute_ssh_command("rm -rf /tmp/*")
