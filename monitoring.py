import subprocess

def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    print(output.decode())
    if error:
        print(error.decode())
    return process.returncode

def get_temp_info():
    cpu_info_command = "cat sys/class/thermal/thermal_zone0/temp"
    result = run_command(cpu_info_command)

    print(result)

def run_stress_test_cpu():
    # push stress file to device
    code = run_command("platform-tools/adb push cpu/stress-android/obj/local/armeabi-v7a/stress /data/local/tmp/stress")
    if code != 0:
        print("Push stress file to device failed")
        return
    
    print("Push stress file to device successfully")

    # change permission
    code = run_command("platform-tools/adb shell chmod 755 /data/local/tmp/stress")
    if code != 0:
        print("Change permission failed")
        return

    # run stress test
    print("Stress test is running...")
    code = run_command("platform-tools/adb shell /data/local/tmp/stress -c 4 -t 10")
    if code != 0:
        print("Run stress test failed")
        return
    print("Run stress test successfully !!!")

if __name__ == "__main__":
    run_stress_test_cpu()
