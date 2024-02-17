from ipregistry import IpregistryClient
from geopy import distance


def get_pc_location():
    client = IpregistryClient("rqp7fvzyerc38rpi")
    ipInfo = client.lookup()
    return ipInfo.location


def distance_between_two_points(pos1, pos2):
    return round(distance.distance(pos1, pos2).km, 2)


def main():
    pc_location = get_pc_location()
    pos1 = (pc_location["latitude"], pc_location["longitude"])
    pos2 = (50.7184, 4.5170)
    print(distance_between_two_points(pos1, pos2))

    if distance_between_two_points(pos1, pos2) < 10:
        return {"success": True, "message": "The phone is near the PC"}
    else:
        return {"success": False, "message": "The phone is not near the PC"}


if __name__ == "__main__":
    print(main())
