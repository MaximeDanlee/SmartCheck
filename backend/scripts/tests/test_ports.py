import os
import sys

from ..utils import send_file_to_device

MOVIE_FILE = "scripts/tests/short_cars.mp4"


def main():
    result = send_file_to_device(file_path=MOVIE_FILE)

    if not result["success"]:
        result["message"] = "File has not been sent"
        return result

    if result["local_file_size"] != result["remote_file_size"]:
        result["success"] = False
        result["message"] = "File has been sent but the file size is different"
        return result

    if result["transfer_rate"] < 1:
        result["success"] = False
        result["message"] = "File has been sent but the transfer rate is too low"
        return result

    result["message"] = "File has been sent successfully"
    return result


if __name__ == "__main__":
    print(main())
