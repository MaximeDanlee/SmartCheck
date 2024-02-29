from .. import constants
from ..utils import run_ssh_command


def find_battery():
    """" Find battery in /sys/class/power_supply/ """
    command = "ls /sys/class/power_supply"
    output, error = run_ssh_command(constants.DEVICE_IP, "pptc", command)

    if error:
        return {"success": False, "message": error}

    battery = None
    for line in output.split("\n"):
        print(line)
        result = get_battery_info(constants.DEVICE_IP, line)

        print(result)

        if result["success"]:
            if result["type"] == "Battery" and result["present"] == "1":
                battery = result
                break

    if battery is None:
        return {"success": False, "message": "Battery not found"}

    return {"success": True, "data": battery, "message": f"Battery state : {battery['health']}"}


def get_battery_info(device, battery="smbb-bif"):
    """ Get battery info from /sys/class/power_supply/ """
    command = f"cat /sys/class/power_supply/{battery}/uevent"
    output, error = run_ssh_command(device, "pptc", command)

    if error:
        return {"success": False, "message": error}

    battery_info = {}
    for line in output.split("\n"):
        if "POWER_SUPPLY_" in line:
            key, value = line.split("=")
            key = key.split("POWER_SUPPLY_")[1].lower()
            battery_info[key] = value

    battery_info["success"] = True
    return battery_info


def main(device=constants.DEVICE_IP):
    battery_info = find_battery()
    if battery_info["success"]:
        battery_info["message"] = "Battery found"
        return battery_info
    else:
        return battery_info


if __name__ == "__main__":
    print("Running battery test")
    print(main())
