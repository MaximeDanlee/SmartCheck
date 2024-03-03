import subprocess
import paramiko
import os
import time

from dotenv import load_dotenv
from ftplib import FTP

load_dotenv()
PASSWORD = os.getenv("PASSWORD")
DEVICE_IP = os.getenv("DEVICE_IP")
USERNAME = os.getenv("USERNAME")


def run_command(command, verbose=True):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()

    if verbose:
        print(output.decode())
        if error:
            print(error.decode())

    return process.returncode


def run_ssh_command_sudo(host=DEVICE_IP, username=USERNAME, password=PASSWORD, command="ls"):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, username=username, password=password)

        command = "sudo -S -p '' %s" % command
        stdin, stdout, stderr = ssh.exec_command(command=command)
        stdin.write(password + "\n")
        stdin.flush()

        # read the standard output and print it
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')

        return output, error

    except Exception as e:
        print("Error:", str(e))
        return None, str(e)
    finally:
        ssh.close()


def run_ssh_command(host=DEVICE_IP, username=USERNAME, command="ls", password=PASSWORD):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(host, username=username, password=password)
        # execute the command
        stdin, stdout, stderr = ssh.exec_command(command)

        # read the standard output and print it
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')

        return output, error

    except Exception as e:
        print("Error:", str(e))
        return None, str(e)
    finally:
        ssh.close()


def file_exists(path):
    try:
        with open(path, 'r') as f:
            return True
    except FileNotFoundError as e:
        return False


def write_to_file(result, path):
    with open(path, "a") as f:
        f.write(result)


def rm_if_file_exists(sftp, remote_file_path):
    try:
        sftp.stat(remote_file_path)
        sftp.remove(remote_file_path)
    except FileNotFoundError:
        pass


def send_file_ftp(host=DEVICE_IP, username=USERNAME, password=PASSWORD, file_path=""):
    ftp = FTP()
    ftp.login(username, password)

    with open(file_path, 'rb') as f:
        ftp.storbinary('STOR fichier_distante.txt', f)

    ftp.quit()


def send_file_to_device(host=DEVICE_IP, username=USERNAME, password=PASSWORD, file_path=""):
    try:
        # get name of the file
        file_name = os.path.basename(file_path)

        # get the local file size
        local_file_size = round(os.path.getsize(file_path) / (1024 * 1024), 2)

        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # ignore the host key

        ssh_client.connect(host, username=username, password=password)

        sftp = ssh_client.open_sftp()

        # remove the file if it exists
        rm_if_file_exists(sftp, f"/home/{username}/{file_name}")

        start_time = time.time()
        sftp.put(file_path, f"/home/{username}/{file_name}")
        end_time = time.time()

        # get the file size in mb
        remote_file_size = round(sftp.stat(file_name).st_size / (1024 * 1024), 2)

        # get the transfer rate in mb
        transfer_rate = round((remote_file_size / (end_time - start_time)), 2)

        sftp.close()
        ssh_client.close()

        return {"success": True,
                "data": {
                    "transfer_rate(mb/s)": transfer_rate,
                    "local_file_size(mb)": local_file_size,
                    "remote_file_size(mb)": remote_file_size}
                }
    except Exception as e:
        print("Error:", str(e))
        return {"success": False, "message": str(e)}


if __name__ == "__main__":
    print(PASSWORD)
