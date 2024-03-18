import os
import sys

from ..utils import run_ssh_command_sudo, run_command
from ..response import Response

def ping_test():
    # Get Ip address Raspberry
    command = "ip addr show wlan0 | awk '/inet / {print $2}' | cut -d'/' -f1"
    output, error = run_command(command=command)

    print(f"ping -c 4 -q {output.strip()}")
    command = f"ping -c 4 -q {output.strip()}"
    output, error = run_ssh_command_sudo(command=command)
    print(output)

    if error:
        return Response(message=error)
    
    if "100% packet loss" in output:
        return Response(success=False, message="Network unreachable")

    if "0% packet loss" in output:
        rtt = output.split(" = ")[1].split("/")[1]
        return Response(success=True, message="Device connected successfully", data={"rtt(ms)": rtt})


def connect_to_wifi():
    command = "nmcli d wifi connect raspi-webgui password ChangeMe"
    output, error = run_ssh_command_sudo(command=command)

    if error:
        Response(message="Could not connect to wifi")

    return Response(success=True, message="Connected to wifi")


def disconnect_wifi():
    command = "nmcli d disconnect wlan0"
    output, error = run_ssh_command_sudo(command=command)

    if error:
        return Response(message=error)

    return Response(success=True, message="Disconnect")


def main():
    result = connect_to_wifi()

    if not result.success:
        return result

    result = ping_test()
    disco = disconnect_wifi()

    if not disco.success:
        return disco

    return result


if __name__ == "__main__":
    print("Running wifi test")
    print(main())
