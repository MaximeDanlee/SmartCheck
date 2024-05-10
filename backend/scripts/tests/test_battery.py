import os
from ..utils import run_ssh_command
from ..response import Response
from dotenv import load_dotenv

load_dotenv()
DEVICE_IP = os.getenv("DEVICE_IP")


def find_battery(device):
    """" Find battery in /sys/class/power_supply/ """
    command = "ls /sys/class/power_supply"
    output, error = run_ssh_command(host=device, command=command)

    if error:
        return Response(message=error)

    battery = None
    for line in output.split("\n"):
        result = get_battery_info(device=device, battery=line)

        if result["success"]:
            if result["type"] == "Battery" and result["present"] == "1":
                result.pop("success")
                battery = result
                break

    if battery is None:
        return Response(message="Battery not found")

    return Response(success=True, data=battery, message=f"Battery state : {battery['health']}")


def get_battery_info(device=DEVICE_IP, battery="smbb-bif"):
    """ Get battery info from /sys/class/power_supply/ """
    command = f"cat /sys/class/power_supply/{battery}/uevent"
    output, error = run_ssh_command(host=device, command=command)

    if error:
        return Response(message=error)

    battery_info = {}
    for line in output.split("\n"):
        if "POWER_SUPPLY_" in line:
            key, value = line.split("=")
            key = key.split("POWER_SUPPLY_")[1].lower()
            battery_info[key] = value

    battery_info["success"] = True
    return battery_info


def main(device=DEVICE_IP):
    return find_battery(device)


if __name__ == "__main__":
    print("Running battery test")
    print(main())
