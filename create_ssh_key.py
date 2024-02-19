import paramiko
import os
from dotenv import load_dotenv

import constants


def create_and_transfer_ssh_key(phone_ip, phone_user, password):
    # Variables
    key_filename = "id_rsa"
    local_key_path = os.path.expanduser(f"~/.ssh/{key_filename}")
    remote_key_path = "/tmp/"

    # Create SSH key if not exists
    if not os.path.exists(local_key_path):
        os.system(f"ssh-keygen -t rsa -b 2048 -f {local_key_path} -N ''")

    # Transfer SSH key to phone
    transport = paramiko.Transport((phone_ip, 22))
    transport.connect(username=phone_user, password=password)

    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.put(f"{local_key_path}.pub", f"{remote_key_path}{key_filename}.pub")
    sftp.close()

    # Adjust permissions
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(phone_ip, username=phone_user, password=password)

    ssh.exec_command(
        f"mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat {remote_key_path}{key_filename}.pub >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys")

    # Remove SSH key from phone
    ssh.exec_command(f"rm {remote_key_path}{key_filename}.pub")

    ssh.close()
    transport.close()

    print("SSH key created and transferred successfully")


if __name__ == "__main__":
    phone_ip = "172.16.42.1"
    phone_user = constants.USERNAME
    # load password from .env file
    load_dotenv()
    phone_password = os.getenv("PASSWORD")

    create_and_transfer_ssh_key(phone_ip, phone_user, phone_password)
