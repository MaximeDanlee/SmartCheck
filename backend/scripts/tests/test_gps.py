from ipregistry import IpregistryClient
from geopy import distance
from .test_4g import configure_4g
from ..utils import run_ssh_command_sudo


def get_pc_location():
    client = IpregistryClient("rqp7fvzyerc38rpi")
    ipInfo = client.lookup()
    return ipInfo.location


def distance_between_two_points(pos1, pos2):
    return round(distance.distance(pos1, pos2).km, 2)


def configure_gps():
    command = "mmcli -m any --location-enable-gps-nmea"
    output, error = run_ssh_command_sudo(command=command)

    if error:
        return {"success": False, "message": error}

    command = "mmcli -m any --location-enable-gps-raw"
    output, error = run_ssh_command_sudo(command=command)

    if error:
        return {"success": False, "message": error}

    return {"success": True, "message": "GPS is enabled"}


def get_gps_info():
    command = "mmcli -m any --location-get"
    output, error = run_ssh_command_sudo(command=command)

    if error:
        return {"success": False, "message": error}

    if "GPS" in output:
        return {"success": True, "message": "GPS is enabled", "data": {}}


def main():
    result = configure_4g()
    if not result["success"]:
        return result

    result = configure_gps()
    if not result["success"]:
        return result

    return get_gps_info()


if __name__ == "__main__":
    print(main())
