import tests.test_cpu as test_cpu
import constants
from tests import test_ports, test_4g


def modem(device=constants.DEVICE_IP):
    modem_result = test_4g.main()

    if modem_result["success"]:
        print("Modem: [OK]")
        print(modem_result["message"])
    else:
        print("Modem: [KO]")
        print(modem_result["message"])


def cpu(device=constants.DEVICE_IP):
    cpu_result = test_cpu.main(device=device)

    if cpu_result["success"]:
        print("CPU: [OK]")
    else:
        print("CPU: [KO]")


def usb_port(device=constants.DEVICE_IP):
    print("USB Port test is running..")
    result = test_ports.main()

    if result["success"]:
        print("USB Port: [OK]")
        print(result["message"])
    else:
        print("USB Port: [KO]")
        print(result["message"])


if __name__ == "__main__":
    # CPU
    # cpu()
    # USB Port
    # usb_port()

    # TODO: GPU

    # TODO: Modem (3G/4G)
    modem()

    # TODO: Wifi

    ## TODO: Screen ###

    ## TODO: GPS ###

    ## TODO: port USB ###
