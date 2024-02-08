import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(f"{__file__}/tests"))))

from utils import send_file_to_device
import constants as constants


def main():
    result = send_file_to_device(constants.DEVICE_IP, "pptc", "", "tests/cars.mp4")

    if result["success"] and (result["local_file_size"] == result["remote_file_size"]):
        return {"success": True, "transfer_rate": result["transfer_rate"], "message": "File has been sent successfully"}
    else:
        return {"success": False, "transfer_rate": result["transfer_rate"], "message": "File size is not the same"}


if __name__ == "__main__":
    main()
