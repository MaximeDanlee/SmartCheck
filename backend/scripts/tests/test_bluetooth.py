from ..utils import run_command, run_ssh_command_sudo
from ..response import Response
import time


def get_MAC_Addr():
    command = "hciconfig hci0 | grep 'BD Address'"
    output, error = run_command(command=command)

    if error:
        return Response(message=error)

    if not output:
        return Response(message="Bluetooth not found")
    
    adress = output.split('BD Address: ')[1].split()[0]
    print(adress)
    return adress

  
def computer_bluetooth():
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
        
    return Response(success=True, message="Pairing succeed")


def phone_bluetooth():
    adress = get_MAC_Addr()

    print("Phone test")

    if isinstance(adress, Response):
        return adress
    
    command = "rc-service bluetooth start"
    output, error = run_ssh_command_sudo(command=command)

    list_command = [
        "bluetoothctl power on",
        "bluetoothctl agent on",
        "bluetoothctl default-agent",
        "bluetoothctl pairable on",
        "bluetoothctl discoverable on",
        "bluetoothctl scan bredr"
        ]

    for command in list_command:
        output, error = run_ssh_command_sudo(command=command)

        if error:
            return Response(message=error)
        
    # Try to pair
    command = f"bluetoothctl pair {adress}"
    output, error = run_ssh_command_sudo(command=command)
    print(output)

    if error:
        Response(message=error)

    count=0
    while "not available" in output and count < 60:
        time.sleep(1)
        # scan on
        # command = f"bluetoothctl scan bredr"
        # output, error = run_ssh_command_sudo(command=command)
        # try to pair devices
        command = f"bluetoothctl pair {adress}"
        output, error = run_ssh_command_sudo(command=command)
        print(output)
        count += 1

    if count == 60 or f"Attempting to pair with {adress}" not in output:
        return Response(message="Pairing failed")

    return Response(success=True, message="Pairing succeed")


def main():
    result = computer_bluetooth()

    if not result.success:
        return result

    result = phone_bluetooth()
    return result
    

if __name__ == "__main__":
    main()