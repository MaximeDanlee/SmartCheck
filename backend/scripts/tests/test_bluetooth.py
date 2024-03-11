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
        "power on"
        "agent on"
        "default-agent",
        "pairable on",
        "discoverable on",
        ]

    for command in list_command:
        output, error = run_command(command=command)

        if error:
            return Response(message=error)
        
    return Response(success=True, message="Pairing succeed")

def phone_bluetooth():
    adress = get_MAC_Addr()

    if isinstance(adress, Response):
        return adress

    list_command = [
        "power on"
        "agent on"
        "default-agent",
        "pairable on",
        "discoverable on",
        "scan on"
        ]

    for command in list_command:
        output, error = run_ssh_command_sudo(command=command)

        if error:
            return Response(message=error)
        
    # Try to pair
    command = f"pair {adress}"
    output, error = run_ssh_command_sudo(command=command)

    if error:
        Response(message=error)

    count=0
    while "not available" in output and count < 30:
        time.sleep(1)
        command = f"pair {adress}"
        output, error = run_ssh_command_sudo(command=command)
        cout += 1

    if count == 30:
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