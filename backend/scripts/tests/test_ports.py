from ..utils import send_file_to_device, upload_file_via_ftp

MOVIE_FILE = "scripts/tests/short_cars.mp4"


def main():
    result = upload_file_via_ftp(file_path=MOVIE_FILE)

    print(result)

    if not result.success:
        return result

    if result.data["local_file_size(MB)"] != result.data["remote_file_size(MB)"]:
        result.success = False
        result.message = "File has been sent but the file size is different"
        return result

    if result.data["transfer_rate(MB/s)"] < 1:
        result.success = False
        result.message = "File has been sent but the transfer rate is too low"
        return result

    result.message = "File has been sent successfully"
    return result


if __name__ == "__main__":
    print(main())
