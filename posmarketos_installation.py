import subprocess
import shlex

def run_command_fastboot(command, device, verbose=True):
    command_list = shlex.split(command)
    result = subprocess.run(["./platform-tools/fastboot", "-s", device, *command_list], capture_output=True, text=True)

    if verbose:
        print(result.stderr)

    if result.stderr.find("OKAY") != -1:
        print("Command executed")
    else:
        print("Command not executed")

def get_device():
    try:
        lines = subprocess.run(["./platform-tools/fastboot", "devices"], capture_output=True, text=True).stdout.split("\n")

        devices = []
        for line in lines:
            if line.find("\t") != -1:
                devices.append(line.split("\t")[0])
        return devices[0]
    
    except Exception as e:
        print(f"An error occurred: {e}")

def unlock_bootloader(device):
    run_command_fastboot("oem unlock", device)

if __name__ == "__main__":
    device = get_device()
    unlock_bootloader(device)