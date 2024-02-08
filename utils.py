import subprocess
import paramiko

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

# send directory via ssh
def send_file_to_device(device, file_path):
    command = ["scp", "-r", file_path, f"pptc@{device}:/home/pptc/"]
    run_command(command)