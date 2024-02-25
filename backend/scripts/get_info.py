import re
from .utils import run_ssh_command
from .constants import USERNAME, DEVICE_IP


# get device info about the device and bootloader
def get_device_info(device):
    # device info
    device_info_keys = [
        # "deviceinfo_format_version",
        "deviceinfo_name",
        "deviceinfo_manufacturer",
        "deviceinfo_codename",
        "deviceinfo_year",
        # "deviceinfo_dtb",
        # "deviceinfo_append_dtb",
        "deviceinfo_arch",
        # "deviceinfo_chassis",
        "deviceinfo_keyboard",
        "deviceinfo_external_storage",
        "deviceinfo_screen_width",
        "deviceinfo_screen_height",
        # "deviceinfo_getty",
        # "deviceinfo_mesa_driver",
        # "deviceinfo_gpu_accelerated"
    ]

    device_info = {}

    # get device info
    command = "cat /usr/share/deviceinfo/deviceinfo"
    output, error = run_ssh_command(device, USERNAME, command)
    if output:
        for line in output.split("\n"):
            for key in device_info_keys:
                if key in line:
                    device_info[key.replace("deviceinfo_", "")] = line.split("=")[1].replace("\"", "").strip()

    # get device mac address
    output, error = run_ssh_command(device, USERNAME, "ip link show wlan0 | awk '/link\/ether/ {print $2}'")
    if output:
        device_info["mac_address"] = output.strip()

    return device_info


def get_cpu_info(device):
    # get cpu info
    cpu_info_keys = [
        "Architecture",
        "Byte Order",
        "CPU(s)",
        "On-line CPU(s) list",
        "Vendor ID",
        "Model name",
        "Model",
        "Thread(s) per core",
        "Core(s) per socket",
        "Socket(s)",
        "Stepping",
        "BogoMIPS"
    ]

    command = "lscpu"
    output, error = run_ssh_command(device, USERNAME, command)
    if output:
        cpu_info = {}
        for line in output.split("\n"):
            for key in cpu_info_keys:
                if key in line:
                    cpu_info[key] = line.split(":")[1].strip()
        return cpu_info


def get_memory_info(device):
    # get memory info
    command = "free -h"
    output, error = run_ssh_command(device, USERNAME, command)

    if output:
        lines = output.split('\n')
        header = re.split(r'\s+', lines[0].strip())
        mem = re.split(r'\s+', lines[1].strip())
        swap = re.split(r'\s+', lines[2].strip())

        # Remove the first element as it's an empty string
        mem.pop(0)
        swap.pop(0)

        # Create a dictionary using header as keys and values as values
        result_dict = dict(zip(header, mem))
        result_dict['swap_total'] = swap[0]
        result_dict['swap_used'] = swap[1]
        result_dict['swap_free'] = swap[2]

        return result_dict

    return None


def get_storage_info(device):
    # get storage info
    command = "df -h"
    output, error = run_ssh_command(device, USERNAME, command)
    if output:
        lines = output.split('\n')
        header = re.split(r'\s+', lines[0].strip())
        storage = []

        for line in lines[1:]:
            temp = re.split(r'\s+', line.strip())
            if temp[len(temp) - 1] == '/':
                storage = temp
                break

        # Remove the first element as it's an empty string
        header.pop(0)

        # Create a dictionary using header as keys and values as values
        result_dict = dict(zip(header, storage))
        return result_dict

    return None


def get_modem_info(device):
    # get modem 4G info
    command = "mmcli -m any -K"
    output, error = run_ssh_command(device, USERNAME, command)

    modem_info = {
        "device-identifier",
        "manufacturer",
        "model",
        "primary-port",
        "modem.generic.state",
        "state-failed-reason",
        "access-technologies.value",
        "supported-ip-families.value",
        "enabled-locks.value",
        "operator-name",
        "apn",
        "ip-type",
        "user",
        "password",
        "own-numbers.value"
    }

    result = {}

    if output:
        lines = output.split('\n')

        for line in lines:
            info = line.split(":")
            if len(info) > 1:
                key = info[0].strip()
                value = info[1].strip()

                if key == "model" and value != 0:
                    return result

                for selected_key in modem_info:
                    if selected_key in key:
                        result[selected_key] = value

    return result


def get_wifi_info(device=DEVICE_IP):
    command = "nmcli radio wifi"
    output, error = run_ssh_command(device, USERNAME, command)

    if output.strip() == "enabled":
        return True
    else:
        return False


def show_information(device_info, cpu_info, memory_info, storage_info, modem_info, wifi_info):
    print("Device information:")
    for key in device_info:
        print(f"\t{key}: {device_info[key]}")

    print()

    print("CPU information:")
    for key in cpu_info:
        print(f"\t{key}: {cpu_info[key]}")

    print()

    print("Memory information:")
    for key in memory_info:
        print(f"\t{key}: {memory_info[key]}")

    print()

    print("Storage information:")
    for key in storage_info:
        print(f"\t{key}: {storage_info[key]}")

    print()

    print("Modem information:")
    if len(modem_info) == 0:
        print("\tNo modem found")
    for key in modem_info:
        print(f"\t{key} : {modem_info[key]}")

    print()

    print("Wifi information:")
    print(f"\tWifi_enabled: {wifi_info}")


def main(device="172.16.42.1"):
    device_info = get_device_info(device)
    cpu_info = get_cpu_info(device)
    memory_info = get_memory_info(device)
    storage_info = get_storage_info(device)
    modem_info = get_modem_info(device)
    wifi_info = get_wifi_info(device)

    print("why")

    return {
        "device": device_info,
        "cpu": cpu_info,
        "memory": memory_info,
        "storage": storage_info,
        "modem": modem_info,
        "wifi": wifi_info
    }


if __name__ == "__main__":
    device = DEVICE_IP

    result = main(device)

    show_information(result["device_info"], result["cpu_info"], result["memory_info"], result["storage_info"],
                     result["modem_info"], result["wifi_info"])
