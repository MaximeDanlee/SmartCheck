from flask import Flask
from flask_cors import CORS
import ping3
import scripts.get_info as get_info
import scripts.tests.test_cpu as test_cpu
import scripts.tests.test_ports as test_port
import scripts.tests.test_4g as test_4g
import scripts.constants as constants
import scripts.tests.test_battery as test_battery

app = Flask(__name__)
CORS(app)


def is_connected():
    try:
        response = ping3.ping(constants.DEVICE_IP)
        if response is None:
            return False
        else:
            return True
    except Exception as e:
        print(e)
        return False


@app.route("/api/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/api/search")
def search():
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


@app.route("/api/test/cpu")
def testing_cpu():
    try:
        if not is_connected():
            return {"success": False, "message": "Device not found"}
        return test_cpu.main()
    except Exception as e:
        print(e)
        return {"success": False, "message": str(e)}


@app.route("/api/test/usb_port")
def testing_port():
    try:
        if not is_connected():
            return {"success": False, "message": "Device not found"}
        return test_port.main()
    except Exception as e:
        return {"success": False, "message": str(e)}


@app.route("/api/test/4g")
def testing_4g():
    try:
        if not is_connected():
            return {"success": False, "message": "Device not found"}
        return test_4g.main()
    except Exception as e:
        return {"success": False, "message": str(e)}


@app.route("/api/test/battery")
def testing_battery():
    try:
        if not is_connected():
            return {"success": False, "message": "Device not found"}

        result = test_battery.main()
        print(result)

        return result
    except Exception as e:
        return {"success": False, "message": str(e)}
