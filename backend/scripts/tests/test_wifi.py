import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

from utils import run_ssh_command
import constants as constants


def simple_wifi_test():
    command = "nmcli radio wifi"
    output, error = run_ssh_command(constants.DEVICE_IP, "pptc", command)

    if output.strip() == "enabled":
        return {"success": True, "message": "Wifi is working"}
    else:
        return {"success": False, "message": "Wifi is not working"}


def main():
    result = simple_wifi_test()
    if not result["success"]:
        return result



    return result


if __name__ == "__main__":
    print(main())
