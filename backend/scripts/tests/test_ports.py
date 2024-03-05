from ..utils import send_file_to_device

MOVIE_FILE = "scripts/tests/short_cars.mp4"


def main():
    result = send_file_to_device(file_path=MOVIE_FILE)

    if not result.success:
        return result

    if result.data["local_file_size(mb)"] != result.data["remote_file_size(mb)"]:
        result.success = False
        result.message = "File has been sent but the file size is different"
        return result

    if result.data["transfer_rate(mb/s)"] < 1:
        result.success = False
        result.message = "File has been sent but the transfer rate is too low"
        return result

    result.message = "File has been sent successfully"
    return result


if __name__ == "__main__":
    print(main())
