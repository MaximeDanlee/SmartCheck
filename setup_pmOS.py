
import os
import subprocess

def run_command(command, verbose=True):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()

    if verbose:
        print(output.decode())
        if error:
            print(error.decode())

    if process.returncode == 0:
        print("Command executed")
    else:
        print("Command not executed")

    return process.returncode


# send directory via ssh
def send_file_to_device(device, file_path):
    command = ["scp", "-r", file_path, f"pptc@{device}:/home/pptc/"]
    run_command(command)

def dmidecode(device):
    run_command(["ssh", f"pptc@{device}", "cd dmidecode-3.5 && chmod +x dmidecode"], verbose=False)
    run_command(["ssh", f"pptc@{device}", "./dmidecode -t 4"], verbose=False)

if __name__ == "__main__":
    device = "172.16.42.1"
    # send_file_to_device(device, "dmidecode-3.5")
    dmidecode(device)



