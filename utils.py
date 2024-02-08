import subprocess
import paramiko
import os
import time


def run_command(command, verbose=True):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()

    if verbose:
        print(output.decode())
        if error:
            print(error.decode())

    return process.returncode


def run_ssh_command(host, username, password, command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        if password == "":
            ssh.connect(host, username=username)
        else:
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

def send_file_to_device(host, username, password, file_path):
    try:
        # get name of the file
        file_name = os.path.basename(file_path)

        # get the local file size
        local_file_size = os.path.getsize(file_path)

        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # ignore the host key
        if password == "":
            ssh_client.connect(host, username=username)
        else:
            ssh_client.connect(host, username=username, password=password)

        sftp = ssh_client.open_sftp()

        # remove the file if it exists
        rm_if_file_exists(sftp, f"/home/{username}/{file_name}")

        start_time = time.time()
        sftp.put(file_path, f"/home/{username}/{file_name}")
        end_time = time.time()

        # get the file size
        remote_file_size = sftp.stat(file_name).st_size

        # get the transfer rate in mb
        transfer_rate = ((remote_file_size / (end_time - start_time)) / 1024) / 1024

        sftp.close()
        ssh_client.close()

        return {"success": True,
                "transfer_rate": transfer_rate,
                "local_file_size": local_file_size,
                "remote_file_size": remote_file_size}
    except Exception as e:
        print("Error:", str(e))
        return {"success": False, "error": str(e)}
