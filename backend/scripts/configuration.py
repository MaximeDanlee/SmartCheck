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


def main():
    interfaces = get_interfaces()
    return get_device_ip_adress_for_interfaces(interfaces)


