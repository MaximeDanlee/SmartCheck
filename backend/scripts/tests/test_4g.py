import os
from time import sleep
from dotenv import load_dotenv

from ..utils import run_ssh_command, run_ssh_command_sudo
from ..response import Response


load_dotenv()
PIN_CODE = os.getenv("PIN_CODE")


def configure_4g():
    if PIN_CODE is None:
        return Response(message="PIN code is not set in .env file")

    # Check if pin code is required
    command = "mmcli -m any -K | grep state"
    output, error = run_ssh_command(command=command)

    # If pin code is required then enter pin code
    if "locked" in output:
        command = f"mmcli -i 0 --pin={PIN_CODE}"
        output, error = run_ssh_command_sudo(command=command)

        if error:
            return Response(message=error)

    # Check if connection already exists
    command = "nmcli connection show | grep sim_cart"
    output, error = run_ssh_command(command=command)

    # check if connection exists
    if "sim_cart" not in output:
        # command = "nmcli c delete sim_cart"
        # run_ssh_command_sudo(command=command)
        # Add new connection
        command = "nmcli c add type gsm ifname '*' con-name 'sim_cart' apn 'simbase'"
        output, error = run_ssh_command_sudo(command=command)

        if error:
            return Response(message=error)

    # Connect to 4G
    command = "nmcli r wwan on"
    output, error = run_ssh_command(command=command)

    # get status of device connection
    command = "nmcli device status | grep sim_cart"
    output, error = run_ssh_command_sudo(command=command)

    count = 0

    while "connecting" in output and count < 30:
        sleep(1)
        output, error = run_ssh_command_sudo(command=command)
        count += 1

    if "connected" in output:
        return Response(success=True, message="4G is connected")
    else:
        return Response(success=True, message="4G is not connected")


def ping_test():
    command = "ping -c 4 -q 8.8.8.8"
    output, error = run_ssh_command(command=command)

    if error:
        return Response(message=error)

    if "0% packet loss" in output:
        rtt = output.split(" = ")[1].split("/")[1]
        return Response(success=True, message="Device can connect to the internet", data={"rtt(ms)": rtt})


def main():
    configuration = configure_4g()

    if configuration.success:
        return ping_test()
    else:
        return configuration


if __name__ == '__main__':
    print(main())
