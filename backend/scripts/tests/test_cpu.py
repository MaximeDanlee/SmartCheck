import threading
import time
import os
from dotenv import load_dotenv
from ..utils import run_command, run_ssh_command, file_exists, write_to_file
from ..response import Response
load_dotenv()
DEVICE_IP = os.getenv("DEVICE_IP")

is_running = True
MAX_FREQ = 50
MAX_TEMP = 65.0
freq_info = []
temp_info = []


def get_freq_info(device):
    cpu_info_command = "top -n 1 -b | awk '/^CPU/ {print $2}'"

    while is_running:
        output, error = run_ssh_command(host=device, command=cpu_info_command)
        if error:
            continue
        freq_info.append(output)


def get_temp_info(device):
    temp_info_command = "sensors | grep -A 2 -E 'cpu[0-9]_thermal-virtual-0' | awk '/temp1:/ {print $2}'"

    while is_running:
        output, error = run_ssh_command(host=device, command=temp_info_command)
        if error:
            print(error)
            continue

        current_temp = []
        for line in output.split("\n"):
            if line:
                temp = line[1:-2]
                current_temp.append(float(temp))

        temp_info.append(current_temp)


def run_stress_test_cpu(device):
    # run stress test
    command = "stress-ng --cpu 4 --timeout 30s"
    run_ssh_command(host=device, command=command)


def verify_freq():
    # if first 5 temp are greater than 50% => return False
    first_five_freq = freq_info[:5]
    for freq in first_five_freq:
        freq = freq.split("%")[0]
        print(f"5:{freq}")
        if int(freq) > MAX_FREQ:
            return False

    # if no line is greater than 50% => return False
    over_100 = False
    for freq in freq_info:
        freq = freq.split("%")[0]
        print(f"tot:{freq}")
        if int(freq) > MAX_FREQ:
            over_100 = True
            break

    if not over_100:
        return False

    # if last 5 lines are greater than 50% => return False
    last_five_freq = freq_info[-5:]
    for freq in last_five_freq:
        freq = freq.split("%")[0]
        print(f"-5{freq}")
        if int(freq) > MAX_FREQ:
            return False

    return True


def verify_temp():
    for temp in temp_info:
        for temp2 in temp:
            if temp2 >= MAX_TEMP:
                return False
            
    return True


def main(device=DEVICE_IP):
    time.sleep(10)

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

    print(freq_info)

    print("----")

    print(temp_info)

    if len(freq_info) == 0 or len(temp_info) == 0:
        return Response(success=False, message="Monitoring temperature or frequency failed")

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
