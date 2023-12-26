import subprocess
import threading
import time
from ppadb.client import Client as AdbClient

is_running = True

def file_exists(path):
    try:
        with open(path, 'r') as f:
            return True
    except FileNotFoundError as e:
        return False


def run_command(command, verbose=True):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()

    if verbose:
        print(output.decode())
        if error:
            print(error.decode())

    return process.returncode


def write_to_file(result, path):
    with open(path, "a") as f:
        f.write(result)


def get_temp_info(device):
    # verifiy if file exists
    if file_exists("cpu_percentage.csv"):
        run_command("rm cpu_percentage.csv")

    cpu_info_command = "top -n 1 -b | awk '/user/ {print $2}' | head -n 1"

    while is_running:
        result = device.shell(cpu_info_command)
        write_to_file(result, "informations/cpu_percentage.csv")


def get_device():
    try:
        client = AdbClient(host="127.0.0.1", port=5037)
        devices = client.devices()

        if not devices:
            raise Exception("Aucun appareil n'est connecté.")

        return devices[0]

    except Exception as e:
        print(f"Une erreur s'est produite : {e}")


def run_stress_test_cpu(device):
    # push stress file to device
    device.push("cpu/stress-android/obj/local/armeabi-v7a/stress", "/data/local/tmp/stress")
    print("Push stress file to device successfully")

    # change permission
    command = "chmod 755 /data/local/tmp/stress"
    device.shell(command)

    # Create a new thread for running get_temp_info
    temp_info_thread = threading.Thread(target=get_temp_info, args=(device,))
    temp_info_thread.start()

    time.sleep(5)

    # run stress test
    print("Stress test is running...")
    command = "/data/local/tmp/stress -c 4 -t 10"
    device.shell(command)

    time.sleep(5)

    # Stop get_temp_info thread
    global is_running
    is_running = False
    
    print("Run stress test successfully !!!")

def verifiy_result():
    with open("informations/cpu_percentage.csv", "r") as f:
        lines = f.readlines()

        # if first 5 lines are greater than 50% => return False
        first_five_lines = lines[:5]
        for line in first_five_lines:
            line = line.split("%")[0]
            if int(line) > 50:
                return False

        over_100 = False
        for line in lines:
            line = line.split("%")[0]
            if int(line) > 50:
                over_100 = True
                break

        if not over_100:
            return False

        # if last 5 lines are greater than 50% => return False
        last_five_lines = lines[-5:]
        for line in last_five_lines:
            line = line.split("%")[0]
            if int(line) > 50:
                return False
            
    return True

if __name__ == "__main__":
    device = get_device()
    run_stress_test_cpu(device=device)
    result = verifiy_result()
    print(result)
