import re
from utils import run_ssh_command, send_file_to_device


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
    output, error = run_ssh_command(device, "pptc", "", command)
    if output:
        for line in output.split("\n"):
            for key in device_info_keys:
                if key in line:
                    device_info[key.replace("deviceinfo_", "")] = line.split("=")[1]

    # get device mac address
    output, error = run_ssh_command(device, "pptc", "", "ip link show wlan0 | awk '/link\/ether/ {print $2}'")
    if output:
        device_info["mac_address"] = output.strip()

    # get GPS info
    output, error = run_ssh_command(device, "pptc", "", "mmcli -m any --location-get")
    
    if error:
        device_info["gps_working"] = False
    else:
        device_info["gps_working"] = True

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
    output, error = run_ssh_command(device, "pptc", "", command)
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
    output, error = run_ssh_command(device, "pptc", "", command)

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
    output, error = run_ssh_command(device, "pptc", "", command)
    if output:
        lines = output.split('\n')
        header = re.split(r'\s+', lines[0].strip())
        storage = []

        for line in lines[1:]:
            temp = re.split(r'\s+', line.strip())
            if temp[len(temp)-1] == '/':
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
    command = "mmcli -m any"
    output, error = run_ssh_command(device, "pptc", "", command)

    result = {}
    new_device = None

    if output:
        lines = output.split('\n')
        
        for line in lines:
            if "device id" in line:
                new_device = line.split(":")[1].strip()
                result[new_device] = {}
            elif "state" in line:
                result[new_device]["state"] = line.split(":")[1].strip()
            elif "failed reason" in line:
                result[new_device]["failed reason"] = line.split(":")[1].strip()
            elif "supported" in line:
                result[new_device]["supported"] = line.split(":")[1].strip()

    return result

def get_wifi_info(device):
    command = "nmcli -t -f active,ssid dev wifi"
    output, error = run_ssh_command(device, "pptc", "", command)

    if output:
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
    for key in modem_info:
        print(f"\tModem: {key}")
        for key2 in modem_info[key]:
            print(f"\t{key2}: {modem_info[key][key2]}")
        print()
    
    print()

    print("Wifi information:")
    print(f"\tWifi_working: {wifi_info}")

def main(device="172.16.42.1"):
    device_info = get_device_info(device)
    cpu_info = get_cpu_info(device)
    memorty_info = get_memory_info(device)
    storage_info =  get_storage_info(device)
    modem_info = get_modem_info(device)
    wifi_info = get_wifi_info(device)

    return {
        "device_info": device_info,
        "cpu_info": cpu_info,
        "memory_info": memorty_info,
        "storage_info": storage_info,
        "modem_info": modem_info,
        "wifi_info": wifi_info
    }

if __name__ == "__main__":
    device = "172.16.42.1"

    device_info = get_device_info(device)
    cpu_info = get_cpu_info(device)
    memorty_info = get_memory_info(device)
    storage_info =  get_storage_info(device)
    modem_info = get_modem_info(device)
    wifi_info = get_wifi_info(device)

    show_information(device_info, cpu_info, memorty_info, storage_info, modem_info, wifi_info)
