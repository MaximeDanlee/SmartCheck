import tests.test_cpu as test_cpu
import constants
from tests import test_ports


def modem(device=constants.DEVICE_IP):
    pass


def cpu(device=constants.DEVICE_IP):
    cpu_result = test_cpu.main(device=device)

    if cpu_result["success"]:
        print("CPU: [OK]")
    else:
        print("CPU: [KO]")


def usb_port(device=constants.DEVICE_IP):
    result = test_ports.main()

    if result["success"]:
        print("USB Port: [OK]")
    else:
        print("USB Port: [KO]")


if __name__ == "__main__":
    # CPU
    cpu()
    # USB Port
    usb_port()
    # TODO: GPU

    # TODO: Modem (3G/4G)

    # TODO: Wifi

    ## TODO: Screen ###

    ## TODO: GPS ###

    ## TODO: port USB ###
