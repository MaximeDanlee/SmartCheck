import time

from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
import os
from dotenv import load_dotenv
import asyncio
from scripts.utils import run_ssh_command_X11

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

# List of tests single attribute is used to determine
# if the test must be run alone or with other tests
tests = {
    # "Cpu": {"function": test_cpu.main, "single": False, "waiting": False},
    # # "Ports": {"function": test_port.main, "single": True, "waiting": False},
    # "4G": {"function": test_4g.main, "single": False, "waiting": False},
    # "Battery": {"function": test_battery.main, "single": False, "waiting": False},
    # "GPS": {"function": test_gps.main, "single": False, "waiting": False},
    "Bluetooth": {"function": test_bluetooth.main, "single": True, "waiting": False},
    "Wifi": {"function": test_wifi.main, "single": False, "waiting": False},
    # "Screen": {"function": test_screen.run_glxgears, "exit_function": test_screen.stop_glxgears, "single": False, "waiting": True}
}

def is_connected(device=DEVICE_IP):
    try:
        response = ping3.ping(device)
        if response is None:
            return False
        else:
            return True
    except Exception as e:
        print(e)
        return False


single_is_running = False


def lock():
    global single_is_running
    while single_is_running:
        pass
    single_is_running = True


def unlock():
    global single_is_running
    single_is_running = False


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


''' SocketIO '''
testing = {}
fastboot_devices = {}
devices = {}
MAXIMUM_RERUN = 5
count = {}

def run_waiting_test(device_ip, device, test_name):
    try:
        tests[test_name]["function"](device_ip, device)

        # Ask quesion to the user
        testing[device]['waiting'] = {
            "success": True, 
            "message": f"{test_name} Working ?", 
            "test_name" : test_name,
            "device": device,
            "device_ip": device_ip
        }
        socketio.emit('testing', {"success": True, "message": "update test", "data":testing})
        devices[device]["state"] = "waiting"
        socketio.emit('devices', {"success": True, "message": "Update devices", "data": devices})
        
        while testing[device].get(test_name) == None:
            time.sleep(1)
    
        testing[device].pop('waiting')
        devices[device]["state"] = "testing"
        socketio.emit('devices', {"success": True, "message": "Update devices", "data": devices})
        tests[test_name]["exit_function"](device_ip)
        
    except Exception as e:
       print(e)


@socketio.on('launch_all_test')
def launch_all_test(device, device_ip):
    try:
        # check if the device is connected
        if not is_connected(device_ip):
            result = {"success": False, "message": "ResultDevice not found", "device": device}
            return

        # increment count of rerun
        if device not in count:
            count[device] = 0
        else:
            count[device] += 1

        testing[device] = {}
        devices[device]["state"] = "testing"
        socketio.emit('devices', {"success": True, "message": "Update devices", "data": devices})
        
        print(f"Running all tests for {device_ip}")
        for test_name in tests.keys():
            # if test is screen testing
            if tests[test_name]["waiting"]:
                run_waiting_test(device_ip, device, test_name)
                continue

            # check if the test is single
            if tests[test_name]["single"]:
                # check if a single test is already running
                lock()
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
            
            print(f"Test {test_name} is done, sucess:{result.success}")
            socketio.emit('testing', {"success": True, "message": "update test", "data":testing})

        # send update devices and testing 
        devices[device]["state"] = "done"
        for test in testing[device]:
            if not testing[device][test]["success"]:
                # if number of rerun has been reached, set the device to done
                if count[device] <= MAXIMUM_RERUN:
                    # devices[device]["state"] = "failed"
                    launch_all_test(device, device_ip)
                    return
                else:
                    count.pop(device)

        devices[device]["result"] = testing[device]

        socketio.emit('devices', {"success": True, "message": "Update devices", "data": devices})
        socketio.emit('testing', {"success": True, "message": "update test", "data":testing, "state": "done"})
    except Exception as e:
        devices[device]["state"] = "testing"
        devices[device]["result"] = {"success": False, "messsage": str(e)}

        launch_all_test(device, device_ip)
        # socketio.emit('devices', {"success": True, "message": "Update devices", "data": devices})
        # socketio.emit('testing', {"success": False, "message": str(e), "data":testing})


@socketio.on('launch_test')
def launch_test(test_name, device_ip):
    try:
        # check if the device is connected
        if not is_connected(device_ip):
            result = {"success": False, "message": "ResultDevice not found", "test_name": test_name}
            socketio.emit('test_result', result)
            return

        # check if the test is single
        if tests[test_name]["single"]:
            # check if a single test is already running
            lock()
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
    """ Send message to the client every 5 seconds to update the list of fastboot devices"""
    global fastboot_devices
    try:
        while True:
            result = fastboot.get_devices()
            for device in result.data:
                if device not in fastboot_devices.keys():
                    fastboot_devices[device] = {"state": "ready", "result": None}

            for device in fastboot_devices.keys():
                if device not in result.data and fastboot_devices[device]["state"] != "flashing" :
                    fastboot_devices.pop(device)

            socketio.emit('fastboot_devices',
                          {"success": True, "message": "Update fastboot devices", "data": fastboot_devices})

            time.sleep(1)
    except Exception as e:
        socketio.emit('fastboot_devices', {"success": False, "message": str(e)})
        socketio.start_background_task(get_fastboot_devices)


@socketio.on('get_devices')
def get_devices():
    """ Send message to the client every 5 seconds to update the list of devices"""
    global devices
    try:
        while True:
            result = configuration.main()
            for device in result:
                if device not in devices.keys():
                    # Add device if not already setup
                    devices[device] = {"state": "testing", "result": None, "ip": result[device]}
                    # Run all tests
                    socketio.start_background_task(launch_all_test, device, result[device])
                    # # deactivate sleep mode
                    # command = "gsettings set org.gnome.desktop.session idle-delay 0"
                    # run_ssh_command_X11(command, result[device])

            for device in devices.keys():
                if device not in result:
                    devices.pop(device)

            socketio.emit('devices', {"success": True, "message": "Update devices", "data": devices})
    except Exception as e:
        print(e)
        socketio.emit('devices', {"success": False, "message": str(e)})
        socketio.start_background_task(get_devices)


@socketio.on('waiting_test')
def waiting_test(device, device_ip, response, test_name):
    try:
        if response:
            testing[device][test_name] = {"success": True, "message": f"The {test_name} works well", "data": {}, "test_name" : test_name}
        else:
            testing[device][test_name] = {"success": False, "message": f"The {test_name} does not work", "data": {}, "test_name" : test_name}

        socketio.emit('testing', {"success": True, "message": "update test", "data":testing})
    except Exception as e:
        testing[device][test_name] = {"success": False, "message": str(e), "data": {}, "test_name" : test_name}
        socketio.emit('testing', {"success": True, "message": "update test", "data":testing})


socketio.start_background_task(get_fastboot_devices)
socketio.start_background_task(get_devices)

if __name__ == "__main__":
    socketio.run(app)
