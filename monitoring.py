import subprocess

def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    return output.decode(), error.decode(), process.returncode

def get_temp_info():
    cpu_info_command = "cat sys/class/thermal/thermal_zone0/temp"
    result = run_command(cpu_info_command)

    print(result)

def run_stress_test_cpu():
    # push stress file to device
    run_command("adb push cpu/stress-android/obj/local/armeabi-v7a/stress /data/local/tmp/stress")
    print("Push stress file to device successfully")

    # change permission
    run_command("adb shell chmod 755 /data/local/tmp/stress")

    # run stress test
    print("Stress test is running...")
    run_command("adb shell /data/local/tmp/stress -c 4 -t 10")
    print("Run stress test successfully")

if __name__ == "__main__":
    run_stress_test_cpu()
