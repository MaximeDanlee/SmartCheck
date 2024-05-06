from ..utils import send_file_to_device, upload_file_via_ftp, run_ssh_command, run_command
import os
from ..response import Response
import time
import csv


MOVIE_FILE = "scripts/tests/short_cars.mp4"


# def main():
#     result = upload_file_via_ftp(file_path=MOVIE_FILE)

#     if not result.success:
#         return result

#     if result.data["local_file_size(MB)"] != result.data["remote_file_size(MB)"]:
#         result.success = False
#         result.message = "File has been sent but the file size is different"
#         return result

#     if result.data["transfer_rate(MB/s)"] < 1:
#         result.success = False
#         result.message = "File has been sent but the transfer rate is too low"
#         return result

#     result.message = "File has been sent successfully"
#     return result

def main(device_ip):
    command = "iperf -s -i 1 -V"
    run_ssh_command(host=device_ip, command=command, in_background=True)

    time.sleep(2)
    command = f"iperf -c {device_ip} -i 1 -t 10 -y c -V"
    output, error = run_command(command=command)

    command = "pkill -SIGINT iperf"
    run_ssh_command(host=device_ip, command=command)

    if error and not output:
        Response(message="Error: " + error, success=False)
        
    bandwidth = []
    csv_reader = csv.reader(output.splitlines())
    for row in csv_reader:
        bandwidth.append(int(row[8]))

    average_bandwidth = sum(bandwidth) / len(bandwidth)
    average_bandwidth_MB = round(average_bandwidth / 1048576)

    return Response(success=(average_bandwidth_MB > 50.0), message=f"ports test passed successfully", data={"bandwidth(Mb/s)":average_bandwidth_MB})