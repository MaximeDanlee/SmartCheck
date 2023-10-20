import subprocess

def systrace():
    # The command to get the trace
    command = "adb shell 'cat /sys/kernel/debug/tracing/trace_pipe' > my_trace.html"

    # Execute the command in a shell
    result = subprocess.run(command, shell=True, capture_output=True, text=True)


    # Print the output of the command
    print(result.stdout)


if __name__ == '__main__':
    