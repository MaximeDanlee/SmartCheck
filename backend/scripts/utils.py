import subprocess
import paramiko
import os
import time
from dotenv import load_dotenv
from ftplib import FTP
from .response import Response

load_dotenv()
PASSWORD = os.getenv("PASSWORD")
DEVICE_IP = os.getenv("DEVICE_IP")
USERNAME = os.getenv("USERNAME")


def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()

    return output.decode(), error.decode()


def run_ssh_command_sudo(host=DEVICE_IP, username=USERNAME, password=PASSWORD, command="ls", interface=None):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        if interface:
            host = f"{host}%{interface}"

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
        data_directory = "scripts/data"
        if not os.path.exists(data_directory):
            os.makedirs(data_directory)
            
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


def delete_file_if_exists(hostname, username, password, file_path):
    try:
        ftp = FTP(hostname)
        ftp.login(username, password)

        if file_path in ftp.nlst():
            ftp.delete(file_path)

        ftp.quit()
    except FileNotFoundError as e:
        pass


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

        # get the file size in MB
        remote_file_size = round(sftp.stat(file_name).st_size / (1024 * 1024), 2)

        # get the transfer rate in MB
        transfer_rate = round((remote_file_size / (end_time - start_time)), 2)

        sftp.close()
        ssh_client.close()

        return Response(success=True,
                        data={
                            "transfer_rate(MB/s)": transfer_rate,
                            "local_file_size(MB)": local_file_size,
                            "remote_file_size(MB)": remote_file_size
                        },
                        message="File has been sent successfully")
    except Exception as e:
        return Response(success=False, message=str(e))


def upload_file_via_ftp(host=DEVICE_IP, username=USERNAME, password=PASSWORD, file_path=""):
    try:
        # get name of the file
        file_name = os.path.basename(file_path)

        # delete the file if it exists
        delete_file_if_exists(host, username, password, file_name)

        # get the local file size
        local_file_size = round(os.path.getsize(file_path) / (1024 * 1024), 2)

        # Connect to the FTP server
        ftp = FTP(host)
        ftp.login(username, password)

        # Open the file in binary mode
        with open(file_path, 'rb') as file:
            # Send the file to the FTP server
            start_time = time.time()
            ftp.storbinary(f'STOR {file_name}', file)
            end_time = time.time()

        # Get the file size in mb
        remote_file_size = round(ftp.size(file_name) / (1024 * 1024), 2)

        # Get the transfer rate in mb
        transfer_rate = round((remote_file_size / (end_time - start_time)), 2)

        print("time:", end_time - start_time)

        ftp.quit()

        return Response(success=True,
                        data={
                            "transfer_rate(MB/s)": transfer_rate,
                            "local_file_size(MB)": local_file_size,
                            "remote_file_size(MB)": remote_file_size
                        },
                        message="File has been sent successfully")

    except Exception as e:
        print(e)
        return Response(message=str(e))


if __name__ == "__main__":
    print(PASSWORD)
