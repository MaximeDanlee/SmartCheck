import datetime
from .utils import run_ssh_command, run_ssh_command_X11
import os
import json


def write_result_to_file(device_ip, result):
    command = "mmcli -m any -K | grep imei"
    output, error = run_ssh_command(host=device_ip, command=command)

    if not output or error:
        print("IMEI not found")
        return

    now = datetime.datetime.now()
    current_date = now.strftime("%d-%m-%Y")

    if not os.path.exists("scripts/results"):
        os.makedirs("scripts/results")

    try:
        imei = output.split(":")[1].strip()
        file_path = f"scripts/results/{imei}_{current_date}.json"
        with open(file_path, "w") as file:
            json.dump(result, file)
    except Exception as e:
        print(e)      


def display_result_screen(device_ip, result):
    no_test = len(result.keys())
    no_success = 0
    color = "red"

    for test in result.keys():
        if result[test]["success"]:
            no_success += 1

    if no_success >= round(no_test / 2):
        color = "orange"

    if no_success == no_test:
        color = "green"

    command = f"xmessage -bg {color} -fg white 'Result'"
    output, error = run_ssh_command_X11(host=device_ip, command=command)

    command = "wmctrl -r Xmessage -b add,maximized_vert,maximized_horz"
    output, error = run_ssh_command_X11(host=device_ip, command=command)
    print(output, error)