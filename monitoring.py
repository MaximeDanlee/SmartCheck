import subprocess
import threading
import time
from command import run_command, run_ssh_command

is_running = True
MAX_FREQ = 50
MAX_TEMP = 65.0

def file_exists(path):
    try:
        with open(path, 'r') as f:
            return True
    except FileNotFoundError as e:
        return False

def write_to_file(result, path):
    with open(path, "a") as f:
        f.write(result)

def get_freq_info(device):
    # verifiy if file exists
    file_monitoring = "informations/frequency.csv"
    if file_exists(file_monitoring):
        run_command(f"rm {file_monitoring}")

    cpu_info_command = "top -n 1 -b | awk '/^CPU/ {print $2}'"

    while is_running:
        output, error = run_ssh_command(device, "pptc", "", cpu_info_command)
        if error:
            continue
        write_to_file(output, file_monitoring)

def get_temp_info(device):
    # verifiy if file exists
    file_monitoring = "informations/temperature.csv"
    if file_exists(file_monitoring):
        run_command(f"rm {file_monitoring}")

    temp_info_command = "sensors | grep -A 2 -E 'cpu[0-9]_thermal-virtual-0' | awk '/temp1:/ {print $2}'"

    while is_running:
        output, error = run_ssh_command(device, "pptc", "", temp_info_command)
        if error:
            continue

        current_temp = ""
        for line in output.split("\n"):
            if line:
                temp = line[1:-2]
                current_temp += temp + ","

        current_temp = current_temp[:-1] + "\n"
        write_to_file(current_temp, file_monitoring)

def run_stress_test_cpu(device):
    # TODO: check if stress-ng is already installed
    # run stress test
    print("Stress test is running...")
    command = "stress-ng --cpu 4 --timeout 60s"
    run_ssh_command(device, "pptc", "", command)

    print("Run stress test successfully !!!")

def verifiy_freq():
    # TODO : CPU frequency
    with open("informations/frequency.csv", "r") as f:
        lines = f.readlines()

        # if first 5 lines are greater than 50% => return False
        first_five_lines = lines[:5]
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
        last_five_lines = lines[-5:]
        for line in last_five_lines:
            line = line.split("%")[0]
            if int(line) > MAX_FREQ:
                return False
            
    return True

def verifiy_temp():
    with open("informations/temperature.csv", "r") as f:
        lines = f.readlines()

        for line in lines:
            for temp in line.split(","):
                if float(temp) > MAX_TEMP:
                    return False

    return True

if __name__ == "__main__":
    device = "172.16.42.1"

    # Create a new thread for running get_freq_info
    freq_info_thread = threading.Thread(target=get_freq_info, args=(device,))
    freq_info_thread.start()

    # Create a new thread for running get_temp_info
    temp_info_thread = threading.Thread(target=get_temp_info, args=(device,))
    temp_info_thread.start()

    # run stress test
    time.sleep(5)
    run_stress_test_cpu(device=device)
    time.sleep(5)

    is_running = False
    
    # verifiy result
    print("\nResult:")
    result = verifiy_freq()
    if result:
        print("CPU: [OK]")
    else:
        print("CPU: [KO]")

    result = verifiy_temp()
    if result:
        print("Temp: [OK]")
    else:    
        print("Temp: [KO]")

