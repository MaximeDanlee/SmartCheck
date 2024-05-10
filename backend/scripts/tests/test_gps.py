from ipregistry import IpregistryClient
from geopy import distance
from .test_4g import configure_4g
from ..utils import run_ssh_command_sudo
from ..response import Response
from dotenv import load_dotenv
import os

load_dotenv()
DEVICE_IP = os.getenv("DEVICE_IP")


def get_pc_location():
    client = IpregistryClient("rqp7fvzyerc38rpi")
    ipInfo = client.lookup()
    return ipInfo.location


def distance_between_two_points(pos1, pos2):
    return round(distance.distance(pos1, pos2).km, 2)


def configure_gps(device):
    command = "mmcli -m any --location-enable-gps-nmea"
    output, error = run_ssh_command_sudo(host=device, command=command)

    if error:
        return Response(message=error)

    command = "mmcli -m any --location-enable-gps-raw"
    output, error = run_ssh_command_sudo(host=device, command=command)

    if error:
        return Response(message=error)

    return Response(success=True, message="GPS is enabled")


def get_gps_info(device):
    command = "mmcli -m any --location-get"
    output, error = run_ssh_command_sudo(host=device, command=command)

    if error:
        return Response(message=error)

    if "GPS" in output:
        return Response(success=True, message="GPS is enabled")


def main(device=DEVICE_IP):
    result = configure_4g(device)
    if not result.success:
        return result

    result = configure_gps(device)
    if not result.success:
        return result

    return get_gps_info(device)


if __name__ == "__main__":
    print(main())
