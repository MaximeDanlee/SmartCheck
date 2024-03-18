import subprocess
import csv


def get_info_fast_boot_mode():
    parameters = [
        "battery-status", "battery-voltage", "boot-mode", "build-mode",
        "cidnum", "gencheckpt", "imei", "meid", "modelid",
        "partition-layout", "platform", "product", "security",
        "serialno", "version", "version-baseband", "version-bootloader",
        "version-cpld", "version-main", "version-microp", "version-misc"
    ]
    output_csv = "informations/fastboot_info.csv"

    def get_param_value(param_name):
        result = subprocess.run(["./platform-tools/fastboot", "getvar", param_name], capture_output=True, text=True)
        return result.stderr.split(": ")[1].split("\n")[0]

    def get_oem_info():
        result = subprocess.run(["./platform-tools/fastboot", "oem", 'device-info'], capture_output=True, text=True)
        oem_info = {}
        for line in result.stderr.split("\n"):
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
            if (value != ""):
                csv_writer.writerow([key, value])

    print(f"Informations saved to {output_csv}")


if __name__ == "__main__":
    get_info_fast_boot_mode()
