# Steps to run the tests manually

# 1. Flash the phone
1. Press the volume down button and the power button to enter the bootloader
2. Connect the phone to the computer
3. Flash the phone with the following command (go to the "myThesis/backend/pmos" directory)
```bash
fastboot flash boot lk2nd.img
fastboot flash userdata fairphone-fp2.img
```

# 2. Find the IP address of the phone and connect to it
1. Find the network interface name of the phone

```bash
netstat -i 
```

2. Find the IPv6 address of the phone

```bash
ping -c 2 -I <Interface> ff02::1
ip -6 neigh show dev <Interface>
```

3. Connect to the phone
```bash
ssh pptc@<IPV6>%<Interface>
```

# 3. Activate modem manager
```bash
sudo rc-service modemmanager start
```

# 4. Execute the tests
prerequisites, ensure that you have install the following:  

Package to add  on the Fairphone 
```bash
sudo apk add stress-ng
sudo apk add lm-sensors
sudo apk add xmessage
sudo apk add iperf
sudo apk add freeglut-dev
sudo apk add modemmanager
sudo apk add nano
sudo apk add wmctrl
```

Package to add on computer (Raspberry)
```bash
sudo apt-get update
sudo apt-get install -y android-tools-adb android-tools-fastboot
sudo apt install lshw
sudo apt install iperf
```

## 4.1. Test 4G connection
This guide outlines the steps to manually test the 4G connection on a device.

### Prerequisites
Ensure that you have the following:

- The device's IP address
- The device's PIN code
- The device has a SIM card with an active data plan

### Steps

1. **Check if PIN code is required**

    Run the following command on the device:

    ```bash
    mmcli -m any -K | grep state
    ```

    If the output contains "locked", proceed to the next step. Otherwise, skip to step 3.

2. **Enter PIN code**

    If the PIN code is required, run the following command on the device:

    ```bash
    mmcli -i 0 --pin=<PIN_CODE>
    ```

    Replace `<PIN_CODE>` with the actual PIN code.

4. **Add new connection**

    Run the following command on the device:

    ```bash
    nmcli c add type gsm ifname '*' con-name 'sim_cart' apn 'simbase'
    ```

5. **Connect to 4G**

    Run the following command on the device:

    ```bash
    nmcli r wwan on
    ```

6. **Check device connection status**

    Run the following command on the device:

    ```bash
    nmcli device status | grep sim_cart
    ```

    Wait until the output contains "connected".

7. **Ping test**

    Run the following command on the device:

    ```bash
    ping -I wwan0 -c 4 -q 8.8.8.8
    ```

    If the output contains "0% packet loss", the device can connect to the internet via 4G.

## 4.2. Test Battery
This guide outlines the steps to manually test the battery on a device.

### Prerequisites

Ensure that you have the following:

- The device's IP address

### Steps

1. **Find battery in /sys/class/power_supply/**

    Run the following command on the device:

    ```bash
    ls /sys/class/power_supply
    ```

    This command lists all the power supplies available on the device. Look for the one that corresponds to the battery.

2. **Get battery info from /sys/class/power_supply/**

    Once you have identified the correct power supply for the battery, you can get its information with the following command:

    ```bash
    cat /sys/class/power_supply/<BATTERY>/uevent
    ```
   
## 4.3. Test Bluetooth
This guide outlines the steps to manually test the Bluetooth connection on a device.

### Prerequisites

Ensure that you have the following:

- The device's IP address
- The device's MAC address

### Steps

1. **Activate Bluetooth**

    Run the following command on the phone:

    ```bash
    rc-service bluetooth start
    ```

2. **Get MAC Address**

    Run the following command on the device:

    ```bash
    hciconfig hci0 | grep 'BD Address'
    ```

    This command will display the MAC address of the Bluetooth device.

3. **Enter Bluetooth Control**

    Run the following command on the device and phone:

    ```bash
    bluetoothctl
    ```

4. **Set Bluetooth Settings**

    Run the following commands on the computer:

    ```bash
    power on
    agent on
    default-agent
    pairable on
    discoverable on
    ```
   
5. **Set Bluetooth Settings**

    Run the following commands on the phone:

    ```bash
    power on
    agent on
    default-agent
    pairable on
    discoverable on
    scan on
    ```
   
6. **Pairing**

    Run the following command on the device:

    ```bash
    pair <MAC_ADDRESS>
    ```

    Replace `<MAC_ADDRESS>` with the actual MAC address of the device you want to pair with. If the pairing is successful, you will see a message saying "Pairing with `<MAC_ADDRESS>` succeeded".

## 4.4. Test CPU
This guide outlines the steps to manually test the CPU on a device.

### Prerequisites

Ensure that you have the following:

- The device's IP address

### Steps

1. **Monitor CPU Frequency**

    Run the following command on the device:

    ```bash
    top -n 1 -b | awk '/^%Cpu/ {print $2}'
    ```

    This command will display the current CPU frequency. Monitor this value before, during, and after the stress test.

2. **Monitor CPU Temperature**

    Run the following command on the device:

    ```bash
    sensors | grep -A 2 -E 'cpu[0-9]_thermal-virtual-0' | awk '/temp1:/ {print $2}'
    ```

    This command will display the current CPU temperature. Monitor this value before, during, and after the stress test.

3. **Run Stress Test**

    Run the following command on the device:

    ```bash
    stress-ng --cpu 4 --timeout 30s
    ```

    This command will stress the CPU for 30 seconds.

4. **Verify CPU Frequency and Temperature**

    After the stress test, check the CPU frequency and temperature again. The frequency should have increased during the stress test and then decreased afterwards. The temperature should not exceed the maximum safe temperature (65 degrees) for the CPU.

## 5. Test GPS
This guide outlines the steps to manually test the GPS on a device.

### Prerequisites

Ensure that you have the following:

- The device's IP address

### Steps

1. **Enable GPS NMEA**

    Run the following command on the device:

    ```bash
    mmcli -m any --location-enable-gps-nmea
    ```

    This command enables the GPS NMEA on the device.

2. **Enable GPS Raw**

    Run the following command on the device:

    ```bash
    mmcli -m any --location-enable-gps-raw
    ```

    This command enables the GPS raw data on the device.

3. **Get GPS Info**

    Run the following command on the device:

    ```bash
    mmcli -m any --location-get
    ```

    This command retrieves the GPS information from the device. If the output contains "GPS", it means the GPS is enabled and working correctly.

## 6. Test USB Port

This guide outlines the steps to manually test the USB Port on a device.

### Prerequisites
Ensure that you have the following:

- The device's IP address

### Steps

1. **Start iperf server on the device**

    Run the following command on the phone:

    ```bash
    iperf -s -i 1 -V
    ```

    This command starts an iperf server on the phone.

2. **Wait for the server to start**

    Wait for a few seconds to ensure the server has started.

3. **Run iperf client on your machine**

    Run the following command on your machine:

    ```bash
    iperf -c <DEVICE_IP> -i 1 -t 10 -y c -V
    ```

    Replace `<DEVICE_IP>` with the actual IP address of the device. This command runs an iperf client on your machine and connects it to the server on the device.  

4. **Stop iperf server on the device**

    Stop the iperf server on the device by pressing `Ctrl+C`.

5. **Check the bandwidth**

    The output of the iperf client command will include the bandwidth of the connection. If the bandwidth is greater than 50 Mb/s, the USB port is working correctly.

Please replace `<DEVICE_IP>` with the actual IP address of the device.

### 7. Test Screen
This guide outlines the steps to manually test the screen on a device.
## Prerequisites

Ensure that you have the following:

- The device's IP address

### Steps

1. **Unlock the Session**

    Run the following command on the device:

    ```bash
    loginctl unlock-session $(loginctl | grep seat0 | awk '{print $1}')
    ```

    This command unlocks the session on the device if needed.

2. **Send the glxgears_custom File to the Device**

    Use a secure copy command to send the `glxgears_custom` file to the device:

    ```bash
    scp myThesis/backend/pmos/glxgears_custom pptc@<DEVICE_IP>%<Interface>:~
    ```
   
3. **Make glxgears_custom Executable**

    Run the following command on the device:

    ```bash
    chmod +x glxgears_custom
    ```

    This command makes the `glxgears_custom` file executable.

4. **Run glxgears_custom**

    Run the following command on the device:

    ```bash
    ./glxgears_custom -text <DEVICE_NAME> -fullscreen
    ```

    Replace `<DEVICE_NAME>` with the actual name of the device. This command runs the `glxgears_custom` program in fullscreen mode.

5. **Stop glxgears_custom**  
    Press `Ctrl+C` to stop the `glxgears_custom` program.

## 8. Test WiFi

This guide outlines the steps to manually test the WiFi on a device.

### Prerequisites

Ensure that you have the following:

- The device's IP address

### Steps

1. **Connect to WiFi**

    Run the following command on the device:

    ```bash
    nmcli d wifi connect raspi-webgui password ChangeMe
    ```

    This command connects the device to the WiFi network with the SSID `raspi-webgui` and the password `ChangeMe`.

2. **Ping Test**

    Run the following command on the device:

    ```bash
    ping -c 4 -q $(ip addr show wlan0 | awk '/inet / {print $2}' | cut -d'/' -f1)
    ```

    This command pings the device's own IP address 4 times. If the output contains "0% packet loss", it means the WiFi is working correctly.

3. **Disconnect WiFi**

    Run the following command on the device:

    ```bash
    nmcli d disconnect wlan0
    ```

    This command disconnects the device from the WiFi network.