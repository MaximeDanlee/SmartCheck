"""
This is the main Flask application file for the backend of the thesis project.
It includes routes for API endpoints and SocketIO event handlers.
The file also defines a list of tests to be executed and provides functions for running the tests.
"""

import time
import threading

from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
import os
from dotenv import load_dotenv
import asyncio
from scripts.result import write_result_to_file, display_result_screen
from scripts.utils import run_ssh_command_X11, run_ssh_command_sudo, run_ssh_command, ping6

import ping3
import scripts.fastboot as fastboot
import scripts.utils as utils
import scripts.configuration as configuration
import scripts.get_info as get_info
import scripts.tests.test_cpu as test_cpu
import scripts.tests.test_ports as test_port
import scripts.tests.test_4g as test_4g
import scripts.tests.test_battery as test_battery
import scripts.tests.test_gps as test_gps
import scripts.tests.test_bluetooth as test_bluetooth
import scripts.tests.test_wifi as test_wifi
import scripts.tests.test_screen as test_screen

load_dotenv()
DEVICE_IP = os.getenv("DEVICE_IP")

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

"""
List of tests single attribute is used to determine
if the test must be run alone or with other tests.
waiting attribute is used to determine if the test
needs a user response.
if waiting is true, an exit_function must be defined
"""
tests = {
    "Cpu": {"function": test_cpu.main, "single": False, "waiting": False},
    "USB Ports": {"function": test_port.main, "single": False, "waiting": False},
    "4G": {"function": test_4g.main, "single": False, "waiting": False},
    "Battery": {"function": test_battery.main, "single": False, "waiting": False},
    "GPS": {"function": test_gps.main, "single": False, "waiting": False},
    "Bluetooth": {"function": test_bluetooth.main, "single": True, "waiting": False},
    "Wifi": {"function": test_wifi.main, "single": False, "waiting": False},
    "Screen_GPU": {"function": test_screen.run_glxgears, "exit_function": test_screen.stop_glxgears, "single": False,
               "waiting": True}
}

''' SocketIO '''
testing = {}
fastboot_devices = {}
devices = {}
MAXIMUM_RERUN = 1
count = {}
device_with_bad_ipv6 = {}
single_is_running = None


def is_connected(device=DEVICE_IP):
    try:
        retry =0
        response = ping6(device)
        while not response and retry < 10:
            retry += 1
            response = ping6(device)
            time.sleep(1)

        if retry >= 10:
            return False
       
        return True
    except Exception as e:
        return False


def lock(device):
    global single_is_running
    while single_is_running is not None and single_is_running in devices:
        pass
    single_is_running = device


def unlock():
    global single_is_running
    single_is_running = None


@app.route("/api/test")
def get_tests_name():
    try:
        return list(tests.keys())
    except Exception as e:
        return {"success": False, "message": str(e)}


@app.route("/api/device_info/<device_ip>")
def get_device_info(device_ip):
    try:
        if not is_connected(device_ip):
            return {"success": False, "message": "ResultDevice not found"}
        result = get_info.main(device_ip)
        if result["device"]["name"] is not None:
            return {"success": True, "message": "ResultDevice found", "data": result}
        else:
            return {"success": False, "message": "ResultDevice found but not supported"}
    except Exception as e:
        return {"success": False, "message": str(e)}


def run_waiting_test(device_ip, device, test_name):
    """
    Runs a waiting test on the specified device.

    Args:
        device_ip (str): The IP address of the device.
        device (str): The name of the device.
        test_name (str): The name of the test to run.
    """
    try:
        tests[test_name]["function"](device_ip, device)

        # Ask question to the user
        testing[device]['waiting'] = {
            "success": True,
            "message": f"{test_name} Working ?",
            "test_name": test_name,
            "device": device,
            "device_ip": device_ip
        }
        socketio.emit('testing', {"success": True, "message": "update test", "data": testing})
        devices[device]["state"] = "waiting"
        socketio.emit('devices', {"success": True, "message": "Update devices", "data": devices})

        while testing[device].get(test_name) is None:
            time.sleep(1)

        testing[device].pop('waiting')
        devices[device]["state"] = "testing"
        socketio.emit('devices', {"success": True, "message": "Update devices", "data": devices})
        tests[test_name]["exit_function"](device_ip)

    except Exception as e:
        print(e)


@socketio.on('launch_all_test')
def launch_all_test(device, device_ip):
    """
    Launch all tests for a specific device.
    
    This function is responsible for running all the tests defined in the 'tests' dictionary for a specific device.
    It first checks if the device is connected, then it runs each test in the 'tests' dictionary.
    If a test is marked as 'single', it will lock the testing system to prevent other tests from running concurrently.
    If a test is marked as 'waiting', it will run the test and wait for user input.
    After each test is run, it sends an update to the client with the test results.
    If all tests are successful, it updates the device state to 'done'.
    If any test fails, it will rerun all tests for the device up to a maximum number of reruns (defined by MAXIMUM_RERUN).
    If the maximum number of reruns is reached, it sets the device state to 'done' and sends the test results to the client.
    
    This function is decorated with the '@socketio.on('launch_all_test')' decorator, which means it is an event handler
    for the 'launch_all_test' event. This event is emitted by the client when it wants to run all tests for a device.
    
    Args:
        device (str): The name of the device to run the tests on.
        device_ip (str): The IP address of the device to run the tests on.
    """
    try:
        if device not in count.keys():
            count[device] = 0
        else:
            count[device] += 1

        if not is_connected(device_ip):
            device_with_bad_ipv6.pop(device)
            devices.pop(device)
            count.pop(device)
            return
        
        testing[device] = {}
        devices[device]["state"] = "testing"
        socketio.emit('devices', {"success": True, "message": "Update devices", "data": devices})

        print(f"Running all tests for {device_ip}")
        for test_name in tests.keys():
            if tests[test_name]["waiting"]:
                run_waiting_test(device_ip, device, test_name)
                continue

            # check if the test is single
            if tests[test_name]["single"]:
                # check if a single test is already running
                lock(device)
                print(f"{device} is running test: {test_name}")
                result = tests[test_name]["function"](device_ip)
                result.test_name = test_name
                testing[device][test_name] = result.to_json()
                unlock()
            else:
                print(f"{device} is running test: {test_name}")
                result = tests[test_name]["function"](device_ip)
                result.test_name = test_name
                testing[device][test_name] = result.to_json()

            print(f"{device}, Test {test_name} is done, sucess:{result.success}")
            socketio.emit('testing', {"success": True, "message": "update test", "data": testing})

        # send update devices and testing 
        devices[device]["state"] = "done"
        for test in testing[device]:
            if not testing[device][test]["success"]:
                # if number of rerun has been reached, set the device to done
                if count[device] < MAXIMUM_RERUN:
                    # devices[device]["state"] = "failed"
                    # launch_all_test(device, device_ip)
                    thread = threading.Thread(target=launch_all_test, args=(device, device_ip))
                    thread.start()
                    return
                else:
                    count.pop(device)
                    break

        
        devices[device]["result"] = testing[device]
        # Display result file and screen
    
        display_result_screen(device_ip, testing[device])
        write_result_to_file(device_ip, testing[device])

        socketio.emit('devices', {"success": True, "message": "Update devices", "data": devices})
        socketio.emit('testing', {"success": True, "message": "update test", "data": testing, "state": "done"})
    except Exception as e:
        print(f"Error in Run_all_test {e}")
        if device in devices.keys():
            devices[device]["state"] = "testing"
            devices[device]["result"] = {"success": False, "messsage": str(e)}
            launch_all_test(device, device_ip)


@socketio.on('launch_test')
def launch_test(device, test_name, device_ip):
    """
    Launch a specific test for a device.
    Args:
        test_name (str): The name of the test to run.
        device_ip (str): The IP address of the device to run the test on.
    """
    # function body goes here(test_name, device_ip):
    try:
        # check if the device is connected
        if not is_connected(device_ip):
            result = {"success": False, "message": "ResultDevice not found", "test_name": test_name}
            socketio.emit('test_result', result)
            return

        # check if the test is single
        if tests[test_name]["single"]:
            # check if a single test is already running
            lock(device)
            print(f"Running test: {test_name}")
            result = tests[test_name]["function"](device_ip)
            result.test_name = test_name
            socketio.emit("test_result", result.to_json())
            unlock()
            print(f"Test {test_name} is done")
        else:
            print(f"Running test: {test_name}")
            result = tests[test_name]["function"](device_ip)
            result.test_name = test_name
            socketio.emit("test_result", result.to_json())

    except Exception as e:
        socketio.emit('test_result', {"success": False, "message": str(e), "test_name": test_name})


@socketio.on('flash_pmos')
def flash_pmos(device):
    """ Flash PMOS on the device
    :param device: device id
    """
    try:
        result = fastboot.get_devices()
        if device not in result.data:
            return

        fastboot_devices[device]["state"] = "flashing"
        socketio.emit('fastboot_devices', {"success": True, "message": "Flashing PMOS", "data": fastboot_devices})
        result = fastboot.flash_pmos(device)
        if result.success:
            fastboot_devices.pop(device)
            socketio.emit('fastboot_devices', {"success": True, "message": "Flashing PMOS succeeded",
                                               "data": fastboot_devices})
        else:
            fastboot_devices[device]["state"] = "done"
            fastboot_devices[device]["result"] = result.to_json()
            socketio.emit('fastboot_devices', {"success": True, "message": "Flashing PMOS failed",
                                               "data": fastboot_devices})
    except Exception as e:
        socketio.emit('fastboot_devices', {"success": False, "message": str(e)})


@socketio.on('get_fastboot_devices')
def get_fastboot_devices():
    global fastboot_devices
    try:
        while True:
            result = fastboot.get_devices()
            for device in result.data:
                if device not in fastboot_devices.keys():
                    fastboot_devices[device] = {"state": "ready", "result": None}

            for device in fastboot_devices.keys():
                if device not in result.data and fastboot_devices[device]["state"] != "flashing":
                    fastboot_devices.pop(device)

            socketio.emit('fastboot_devices',
                          {"success": True, "message": "Update fastboot devices", "data": fastboot_devices})

            time.sleep(1)
    except Exception as e:
        socketio.emit('fastboot_devices', {"success": False, "message": str(e)})
        socketio.start_background_task(get_fastboot_devices)


@socketio.on('get_testing')
def get_testing():
    try:
        socketio.emit('testing', {"success": True, "message": "update test", "data": testing})
    except Exception as e:
        pass


def configure_device(device_ip):
    # start modemmanager service
    run_ssh_command_sudo(host=device_ip, command="sudo rc-service modemmanager start", timeout=5)
    # deactivate sleep mode
    command = "xfconf-query -c xfce4-power-manager -p /xfce4-power-manager/blank-on-ac -n -t int -s 0"
    output, error = run_ssh_command_X11(host=device_ip, command=command)
    command = "xfconf-query -c xfce4-power-manager -p /xfce4-power-manager/blank-on-battery -n -t int -s 0"
    output, error = run_ssh_command_X11(host=device_ip, command=command)


@socketio.on('get_devices')
def get_devices():
    """ Send message to the client every x seconds to update the list of devices"""
    global devices
    try:
        while True:
            result = configuration.main()
            for device in result:
                # Little trick to avoid running tests on device with bad ipv6, keep only second ipv6 saved
                if device not in device_with_bad_ipv6.keys():
                    device_with_bad_ipv6[device] = {"ip": result[device]}
                else :
                    if device_with_bad_ipv6[device]["ip"] != result[device]:
                        device_with_bad_ipv6[device]["ip"] = result[device]
                        if is_connected(result[device]):
                            configure_device(result[device])
                            devices[device] = {"state": "testing", "result": None, "ip": result[device]}
                            # Run all tests
                            # socketio.start_background_task(launch_all_test, device, result[device])
                            test_thread = threading.Thread(target=launch_all_test, args=(device, result[device]))
                            test_thread.start()
                            
            socketio.emit('devices', {"success": True, "message": "Update devices", "data": devices})
    except Exception as e:
        print(e)
        socketio.start_background_task(get_devices)

def remove_devices():
    while True:
        try:
            for device in devices:
                if not is_connected(devices[device]["ip"]):
                    print(f"REMOVE {device}")
                    devices.pop(device)
                    device_with_bad_ipv6.pop(device)
                    count.pop(device)
        except Exception as e:
            pass
        
        time.sleep(1)


@socketio.on('waiting_test')
def waiting_response(device, device_ip, response, test_name):
    """
    Event handler for the 'waiting_test' event.

    This function is called when the client emits a 'waiting_test' event. It updates the test result for a specific
    test on a specific device based on the user's response. If the user's response is True, it means the test passed.
    If the user's response is False, it means the test failed. The test result is then sent to the client.

    Args:
        device (str): The name of the device the test was run on.
        device_ip (str): The IP address of the device the test was run on.
        response (bool): The user's response to the test. True means the test passed, False means it failed.
        test_name (str): The name of the test that was run.
    """
    try:
        if response:
            testing[device][test_name] = {"success": True, "message": f"The {test_name} works well", "data": {},
                                          "test_name": test_name}
        else:
            testing[device][test_name] = {"success": False, "message": f"The {test_name} does not work", "data": {},
                                          "test_name": test_name}

        socketio.emit('testing', {"success": True, "message": "update test", "data": testing})
    except Exception as e:
        testing[device][test_name] = {"success": False, "message": str(e), "data": {}, "test_name": test_name}
        socketio.emit('testing', {"success": True, "message": "update test", "data": testing})


socketio.start_background_task(get_fastboot_devices)
socketio.start_background_task(get_devices)
socketio.start_background_task(remove_devices)

if __name__ == "__main__":
    socketio.run(app)
