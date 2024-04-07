import time

from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
import os
from dotenv import load_dotenv
import asyncio

import ping3
import scripts.fastboot as fastboot
import scripts.get_info as get_info
import scripts.tests.test_cpu as test_cpu
import scripts.tests.test_ports as test_port
import scripts.tests.test_4g as test_4g
import scripts.tests.test_battery as test_battery
import scripts.tests.test_gps as test_gps
import scripts.tests.test_bluetooth as test_bluetooth
import scripts.tests.test_wifi as test_wifi

load_dotenv()
DEVICE_IP = os.getenv("DEVICE_IP")

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

# List of tests single attribute is used to determine
# if the test must be run alone or with other tests
tests = {
    "Cpu": {"function": test_cpu.main, "single": True},
    "Ports": {"function": test_port.main, "single": True},
    "4G": {"function": test_4g.main, "single": True},
    "Battery": {"function": test_battery.main, "single": False},
    "GPS": {"function": test_gps.main, "single": False},
    "Bluetooth": {"function": test_bluetooth.main, "single": False},
    "Wifi": {"function": test_wifi.main, "single": True}
}


def is_connected():
    try:
        response = ping3.ping(DEVICE_IP)
        if response is None:
            return False
        else:
            return True
    except Exception as e:
        print(e)
        return False


@app.route("/api/search")
def search_device():
    try:
        if not is_connected():
            return {"success": False, "message": "Device not found"}

        result = get_info.main()

        if result["device"]["name"] is not None:
            return {"success": True, "message": "Device found", "data": result}
        else:
            return {"success": False, "message": "Device found but not supported"}
    except Exception as e:
        return {"success": False, "message": str(e)}


# TESTS
@app.route("/api/test")
def get_tests_name():
    try:
        return list(tests.keys())
    except Exception as e:
        return {"success": False, "message": str(e)}


@app.route("/api/fastboot/devices")
def get_fastboot_devices():
    return fastboot.get_devices().to_json()


''' SocketIO '''

single_is_running = False


def lock():
    global single_is_running
    while single_is_running:
        pass
    single_is_running = True


def unlock():
    global single_is_running
    single_is_running = False


@socketio.on('launch_test')
def launch_test(test_name):
    try:
        # check if the device is connected
        if not is_connected():
            result = {"success": False, "message": "Device not found", "test_name": test_name}
            socketio.emit('test_result', result)
            return

        # check if the test is single
        if tests[test_name]["single"]:
            # check if a single test is already running
            lock()
            print(f"Running test: {test_name}")
            result = tests[test_name]["function"]()
            result.test_name = test_name
            socketio.emit("test_result", result.to_json())
            unlock()
            print(f"Test {test_name} is done")
        else:
            print(f"Running test: {test_name}")
            result = tests[test_name]["function"]()
            print(result)
            result.test_name = test_name
            socketio.emit("test_result", result.to_json())

    except Exception as e:
        socketio.emit('test_result', {"success": False, "message": str(e), "test_name": test_name})


fastboot_devices = {}


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
                    fastboot_devices[device] = {"state": "sleeping", "result": None}

            socketio.emit('fastboot_devices',
                          {"success": True, "message": "Update fastboot devices", "data": fastboot_devices})

            time.sleep(5)
    except Exception as e:
        print("wtf")
        socketio.emit('fastboot_devices', {"success": False, "message": str(e)})


socketio.start_background_task(get_fastboot_devices)

if __name__ == "__main__":
    socketio.run(app)
