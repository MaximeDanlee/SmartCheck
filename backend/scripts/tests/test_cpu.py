import threading
import time
import os
from dotenv import load_dotenv
from ..utils import run_command, run_ssh_command, file_exists, write_to_file
from ..response import Response


is_running = True
MAX_FREQ = 50
MAX_TEMP = 65.0
FREQ_FILE = "scripts/data/frequency.csv"
TEMP_FIME = "scripts/data/temperature.csv"

load_dotenv()
DEVICE_IP = os.getenv("DEVICE_IP")


def get_freq_info(device):
    # verify if file exists
    if file_exists(FREQ_FILE):
        run_command(f"rm {FREQ_FILE}")

    cpu_info_command = "top -n 1 -b | awk '/^CPU/ {print $2}'"

    while is_running:
        output, error = run_ssh_command(device, "pptc", cpu_info_command)
        if error:
            continue
        write_to_file(output, FREQ_FILE)


def get_temp_info(device):
    # verify if file exists
    if file_exists(TEMP_FIME):
        run_command(f"rm {TEMP_FIME}")

    temp_info_command = "sensors | grep -A 2 -E 'cpu[0-9]_thermal-virtual-0' | awk '/temp1:/ {print $2}'"

    while is_running:
        output, error = run_ssh_command(device, "pptc", temp_info_command)
        if error:
            print(error)
            continue

        current_temp = ""
        for line in output.split("\n"):
            if line:
                temp = line[1:-2]
                current_temp += temp + ","

        current_temp = current_temp[:-1] + "\n"
        write_to_file(current_temp, TEMP_FIME)


def run_stress_test_cpu(device):
    # TODO: check if stress-ng is already installed
    # run stress test
    command = "stress-ng --cpu 4 --timeout 30s"
    run_ssh_command(device, "pptc", command)


def verify_freq():
    # TODO : CPU frequency
    with open(FREQ_FILE, "r") as f:
        lines = f.readlines()

        # if first 5 lines are greater than 50% => return False
        first_five_lines = lines[:10]
        for line in first_five_lines:
            line = line.split("%")[0]
            if int(line) > MAX_FREQ:
                return False

        over_100 = False
        for line in lines:
            line = line.split("%")[0]
            if int(line) > MAX_FREQ:
                over_100 = True
                break

        if not over_100:
            return False

        # if last 5 lines are greater than 50% => return False
        last_five_lines = lines[-10:]
        for line in last_five_lines:
            line = line.split("%")[0]
            if int(line) > MAX_FREQ:
                return False

    return True


def verify_temp():
    with open(TEMP_FIME, "r") as f:
        lines = f.readlines()

        for line in lines:
            for temp in line.split(","):
                if float(temp) > MAX_TEMP:
                    return False

    return True


def main(device=DEVICE_IP):
    print("Running CPU stress test")
    file_exists(FREQ_FILE)
    # Create a new thread for running get_freq_info
    freq_info_thread = threading.Thread(target=get_freq_info, args=(device,))
    freq_info_thread.start()

    # Create a new thread for running get_temp_info
    temp_info_thread = threading.Thread(target=get_temp_info, args=(device,))
    temp_info_thread.start()

    global is_running
    is_running = True

    # run stress test
    time.sleep(10)
    run_stress_test_cpu(device=device)
    time.sleep(10)

    is_running = False

    freq = verify_freq()
    temp = verify_temp()

    return Response(success=freq and temp, data={"frequency": freq, "temperature": temp},
                    message="CPU stress test has been run successfully")


if __name__ == "__main__":
    print(main())

    # verify result
    print("\nResult:")
    result = verify_freq()
    if result:
        print("Frequency: [OK]")
    else:
        print("Frequency: [KO]")

    result = verify_temp()
    if result:
        print("Temperature: [OK]")
    else:
        print("Temperature: [KO]")
