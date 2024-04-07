import subprocess
import csv
from .utils import run_command
from .response import Response

Fastboot = "./platform-tools-mac/fastboot"


def get_info(device_id):
    parameters = [
        "battery-status", "battery-voltage", "boot-mode", "build-mode",
        "cidnum", "gencheckpt", "imei", "meid", "modelid",
        "partition-layout", "platform", "product", "security",
        "serialno", "version", "version-baseband", "version-bootloader",
        "version-cpld", "version-main", "version-microp", "version-misc"
    ]
    output_csv = "scripts/data/frequency.csv"

    def get_param_value(param_name):
        command = f"{Fastboot} -s {device_id} getvar {param_name}"
        output, error = run_command(command=command)

        if error:
            return Response(message=error)

        return output.split(": ")[1].split("\n")[0]

    def get_oem_info():
        command = f"{Fastboot} -s {device_id} oem device-info"
        output, error = run_command(command=command)
        oem_info = {}
        for line in output.split("\n"):
            if line != "" and line.find(": ") != -1 and line.find("Finished") == -1:
                key, value = line.split(": ")
                oem_info[key] = value

        return oem_info

    # write to csv file
    with open(output_csv, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)

        # Get variables values
        csv_writer.writerow(["Getvar", "Value"])
        for param in parameters:
            value = get_param_value(param)
            if (value != ""):
                csv_writer.writerow([param, value])

        # Get Oem device info
        csv_writer.writerow("")
        csv_writer.writerow(["Oem device info", "Value"])
        for key, value in get_oem_info().items():
            if value != "":
                csv_writer.writerow([key, value])

    print(f"Informations saved to {output_csv}")


def get_devices():
    command = f"{Fastboot} devices"
    output, error = run_command(command=command)

    if error:
        return Response(message=error)

    devices = []
    for line in output.split("\n"):
        if line.find("\t") != -1:
            devices.append(line.split("\t")[0])

    return Response(success=True, message="List of device found", data=devices)


def flash_pmos(device_id):
    print(f"Flashing PostmarketOS on device {device_id}")
    command = f"{Fastboot} -s {device_id} flash boot pmos/lk2nd.img"
    output, error = run_command(command=command)

    if "FAILED" in error:
        return Response(message=error)

    command = f"{Fastboot} -s {device_id} flash userdata pmos/fairphone-fp2.img"
    output, error = run_command(command=command)

    if "FAILED" in error:
        return Response(message=error)

    command = f"{Fastboot} -s {device_id} reboot"
    output, error = run_command(command=command)

    print(f"PostmarkedOS flashed successfully on device {device_id}")

    return Response(success=True, message="PostmarkedOS flashed successfully")


if __name__ == "__main__":
    get_info()
