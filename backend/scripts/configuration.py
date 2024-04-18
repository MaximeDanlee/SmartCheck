from .utils import run_command
from .response import Response


def get_interfaces():
    command = "netstat -i | awk '{print $1}'"
    output, error = run_command(command=command)

    interfaces = []
    for line in output.split("\n"):
        if "usb" in line:
            interfaces.append(line)

    return interfaces


def get_device_ip_adress_for_interfaces(interfaces):
    # discover connected devices
    for interface in interfaces:
        command = f"ping -c 2 -I {interface} ff02::1"
        output, error = run_command(command=command)

    # get ipv6 of connected devices
    ipv6 = {}
    for interface in interfaces:
        command = f"ip -6 neigh show dev {interface}"
        output, error = run_command(command=command)
        if output and not error:
            ipv6[interface] = output.split(" ")[0]

    return ipv6


def get_id_port_usb():
    command = "lshw -C Network"
    output, error = run_command(command=command)

    network_info = {}

    interfaces = output.strip().split('*-network:')

    interfaces = interfaces[1:]

    for interface in interfaces:
        interface_info = {}
        lines = interface.strip().split('\n')
        lines = lines[1:]

        for line in lines:
            if "WARNING" in line:
                pass
            key, value = line.strip().split(':', 1)
            interface_info[key.strip()] = value.strip()
        if 'logical name' in interface_info:
            network_info[interface_info['logical name']] = interface_info

    key_to_remove = []
    # filte port with ip=172.16.42.2
    for key, value in network_info.items():
        if "172.16.42.2" not in value["configuration"]:
            key_to_remove.append(key)

    for key in key_to_remove:
        network_info.pop(key)

    return network_info


def main():
    interfaces = get_interfaces()
    ip_adress = get_device_ip_adress_for_interfaces(interfaces)
    port = get_id_port_usb()
    
    devices = {}
    for key, value in port.items():
        if key in ip_adress:
            devices[value["bus info"]] = f"{ip_adress[key]}%{key}"

    return devices

