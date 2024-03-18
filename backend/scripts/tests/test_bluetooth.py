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

<<<<<<< HEAD
=======
    # Activate blutooth 
    command = "rc-service bluetooth start"
    output, error = run_ssh_command_sudo(command=command)

>>>>>>> master
    # Connexion SSH
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, port, username, password)

    try:
<<<<<<< HEAD
        time.sleep(10)
        channel = ssh.invoke_shell()
        channel.send('bluetoothctl\n')
        time.sleep(1) 
=======
        time.sleep(5)
        channel = ssh.invoke_shell()
        channel.send('bluetoothctl\n')
>>>>>>> master

        list_command = [
            "power on",
            "agent on",
            "default-agent",
            "pairable on",
            "discoverable on",
<<<<<<< HEAD
            "scan bredr"
=======
            "scan on"
>>>>>>> master
        ]
        
        for command in list_command:
            channel.send(f"{command}\n")
            output = channel.recv(1024).decode()
<<<<<<< HEAD
            time.sleep(1)

        time.sleep(10)
        # check if raspberry found
        output = channel.recv(1024).decode()
        if adress not in output:
            return Response(message="Computer bluetooth not found")

        # pairing 
        channel.send(f"pair {adress}\n")

        # check if phone tried to pair
        time.sleep(10)
        output = channel.recv(1024).decode()
        if f"Attempting to pair with {adress}" in output:
            return Response(success=True, message=f"Pairing with {adress} succeeded")

        return Response(message=output)
=======

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
>>>>>>> master
    finally:
        ssh.close()

  
def computer_bluetooth():
<<<<<<< HEAD
=======
    # Activate blutooth 
    output, error = run_command("sudo systemctl restart bluetooth")
    time.sleep(5)

>>>>>>> master
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


def main():
    result = computer_bluetooth()

    if not result.success:
        return result

    return bluetoothctl_pairing()
    

if __name__ == "__main__":
    main()