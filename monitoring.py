import tests.test_cpu as test_cpu
import constants
from tests import test_ports, test_4g


def modem(device=constants.DEVICE_IP):
    print("Modem test is running..")
    modem_result = test_4g.main()

    if modem_result["success"]:
        print("Modem: [OK]")
        print(modem_result["message"])
    else:
        print("Modem: [KO]")
        print(modem_result["message"])

    print()


def cpu(device=constants.DEVICE_IP):
    print("CPU stress test is running...")
    cpu_result = test_cpu.main(device=device)

    if cpu_result["success"]:
        print("CPU: [OK]")
        print(cpu_result["message"])
    else:
        print("CPU: [KO]")
        print(cpu_result["message"])

    print()


def usb_port(device=constants.DEVICE_IP):
    print("USB Port test is running...")
    result = test_ports.main()

    if result["success"]:
        print("USB Port: [OK]")
        print(result["message"])
    else:
        print("USB Port: [KO]")
        print(result["message"])

    print()


if __name__ == "__main__":
    # cpu()
    # usb_port()
    modem()

    # TODO: GPU

    # TODO: Wifi

    # TODO: Screen

    # TODO: GPS
