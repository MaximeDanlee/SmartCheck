from ..utils import run_command, run_ssh_command_sudo
from ..response import Response
import time
from dotenv import load_dotenv
import paramiko
import os

load_dotenv()
PASSWORD = os.getenv("PASSWORD")
DEVICE_IP = os.getenv("DEVICE_IP")
USERNAME = os.getenv("USERNAME")

def get_MAC_Addr():
    command = "hciconfig hci0 | grep 'BD Address'"
    output, error = run_command(command=command)

    if error:
        return Response(message=error)

    if not output:
        return Response(message="Bluetooth not found")
    
    adress = output.split('BD Address: ')[1].split()[0]
    return adress

# This function allows to interact with the shell to enter 
# command in the menu of bluetothctl because "bluetooth scan on"
# doesn't work.
def bluetoothctl_pairing(hostname=DEVICE_IP, port=22, username=USERNAME, password=PASSWORD):
    adress = get_MAC_Addr()
    
    if isinstance(adress, Response):
        return adress

    # Activate blutooth 
    command = "rc-service bluetooth start"
    output, error = run_ssh_command_sudo(host=DEVICE_IP, command=command)

    # Connexion SSH
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, port, username, password)

    try:
        time.sleep(5)
        channel = ssh.invoke_shell()
        channel.send('bluetoothctl\n')

        list_command = [
            "power on",
            "agent on",
            "default-agent",
            "pairable on",
            "discoverable on",
            "scan on"
        ]
        
        for command in list_command:
            channel.send(f"{command}\n")
            output = channel.recv(1024).decode()

        # pairing 
        count = 0
        while f"Attempting to pair with {adress}" not in output:
            channel.send(f"pair {adress}\n")
            output = channel.recv(1024).decode()

            if count == 30:
                return Response(message="Computer bluetooth not found")
            count += 1
            time.sleep(1)

        return Response(success=True, message=f"Pairing with {adress} succeeded")
    finally:
        ssh.close()

  
def computer_bluetooth():
    # Activate blutooth 
    output, error = run_command("sudo systemctl restart bluetooth")
    time.sleep(5)

    list_command = [
        "bluetoothctl power on",
        "bluetoothctl agent on",
        "bluetoothctl default-agent",
        "bluetoothctl pairable on",
        "bluetoothctl discoverable on"
        ]

    for command in list_command:
        output, error = run_command(command=command)

        if error:
            return Response(message=error)
        
    return Response(success=True, message="Computer bluetooth activated")


def main(device=DEVICE_IP):
    global DEVICE_IP
    DEVICE_IP = device

    result = computer_bluetooth()

    if not result.success:
        return result

    return bluetoothctl_pairing(hostname=DEVICE_IP)
    

if __name__ == "__main__":
    main()