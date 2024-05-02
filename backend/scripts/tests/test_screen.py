import os
from time import sleep
from dotenv import load_dotenv
import time

from ..utils import run_ssh_command, run_ssh_command_sudo, run_ssh_command_X11
from ..response import Response

load_dotenv()
DEVICE_IP = os.getenv("DEVICE_IP")

def run_glxgears(device=DEVICE_IP):
    command = "loginctl unlock-session $(loginctl | grep seat0 | awk '{print $1}')"
    output, error = run_ssh_command_sudo(host=DEVICE_IP, command=command)

    time.sleep(5)
    
    command = "glxgears"
    output, error = run_ssh_command_X11(host=DEVICE_IP, command=command)

    print(output)

    # command = "\x03" #(CTRL+C)
    # output, error = run_ssh_command_X11(host=DEVICE_IP, command=command)

def stop_glxgears(device=DEVICE_IP):
    command = "pkill -SIGINT glxgears"
    output, error = run_ssh_command(host=DEVICE_IP, command=command)

def main(device=DEVICE_IP):
    global DEVICE_IP
    DEVICE_IP = device

    run_glxgears()