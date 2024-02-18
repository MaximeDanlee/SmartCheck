from utils import run_ssh_command
from dotenv import load_dotenv
import constants as constants
import os

load_dotenv()
PIN_CODE = os.getenv("PIN_CODE")


def configure_4g():
    command = f"sudo mmcli -i 0 --pin={PIN_CODE}"
    output, error = run_ssh_command(constants.DEVICE_IP, "pptc", "", command)

    if error:
        return {"success": False, "message": error}

    command = "sudo nmcli c add type gsm ifname '*' con-name 'sim_cart' apn 'internet.proximus.be'"
    output, error = run_ssh_command(constants.DEVICE_IP, "pptc", "", command)

    if error:
        return {"success": False, "message": error}

    command = "nmcli r wwan on"
    output, error = run_ssh_command(constants.DEVICE_IP, "pptc", "", command)

    command = "sudo nmcli device status"
    output, error = run_ssh_command(constants.DEVICE_IP, "pptc", "", command)

    for line in output.split("\n"):
        if "sim_cart" in line:
            state = line.split()[2]
            if state == "connected":
                return {"success": True, "message": "4G is connected"}
            else:
                return {"success": False, "message": "4G is not connected"}


def ping_test():
    command = "ping -c 4 -q 8.8.8.8"
    output, error = run_ssh_command(constants.DEVICE_IP, "pptc", "", command)

    if error:
        return {"success": False, "message": error}

    if "0% packet loss" in output:
        rtt = output.split(" = ")[1].split("/")[1]
        print(f"RTT: {rtt} ms")
        return {"success": True, "message": f"RTT: {rtt} ms", "rtt": rtt}


def main():
    configuration = configure_4g()

    if configuration["success"]:
        return ping_test()
    else:
        return configuration


if __name__ == '__main__':
    main()
    ping_test()
