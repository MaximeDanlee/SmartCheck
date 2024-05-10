# Connect via SSH
```bash
ssh pptc@172.16.42.1
```

## connect to multiple Devices solution
https://gitlab.com/postmarketOS/pmaports/-/merge_requests/3349
```bash
ping -c 2 -I usb0 ff02::1
ping -c 2 -I usb1 ff02::1
ip -6 neigh show dev usb0
ip -6 neigh show dev usb1
ssh pptc@<IPV6 for usb0>%usb0
ssh pptc@<IPV6 for usb1>%usb1
```

# Internet over USB PostMarketOS
## On the PostMarketOS phone
```bash
sudo ip route add default via 172.16.42.2 dev usb0
echo nameserver 1.1.1.1 > /etc/resolv.conf
```

If the last command doesn't work you can do it manually with nano:
```bash
nano /etc/resolv.conf
```

## On Linux
First, enable IP forwarding:
```bash
sudo sysctl net.ipv4.ip_forward=1
```
iptables (Ubuntu/Arch/Alpine)
```bash
sudo iptables -A FORWARD -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

sudo iptables -A FORWARD -s 172.16.42.0/24 -j ACCEPT

sudo iptables -A POSTROUTING -t nat -j MASQUERADE -s 172.16.42.0/24

sudo iptables-save #Save changes
```

# Connect phone to wifi
```bash
nmcli d wifi connect <SSID> password <password>
```

```bash
nmcli con add type wifi con-name "eduroam" ifname "wlp4s0" ssid "eduroam" wifi-sec.key-mgmt "wpa-eap" 802-1x.identity "maxime.danlee@student.uclouvain.be" 802-1x.password <password> 802-1x.system-ca-certs "yes" 802-1x.domain-suffix-match "radius.lu.se" 802-1x.eap "peap" 802-1x.phase2-auth "mschapv2"
```

# SIM Cart Manager
Display the status of connected devices
```bash
sudo nmcli device status
```

Add a new connection

Configure pin code
```bash
sudo mmcli -i 0 --pin=1234
```

```bash
nmcli c add type gsm ifname '*' con-name 'sim_cart' apn 'internet.proximus.be'
nmcli r wwan on
```

# Package to add  on the Fairphone 
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
stress-ng,lm-sensors,xmessage,iperf,freeglut-dev,modemmanager,nano,wmctrl


# Package to add  on Raspberry
```bash
sudo apt-get update
sudo apt-get install -y android-tools-adb android-tools-fastboot
sudo apt install lshw
sudo apt install iperf
```

## Install pmboostrap 
```bash
$ git clone --depth=1 https://gitlab.com/postmarketOS/pmbootstrap.git
$ mkdir -p ~/.local/bin
$ ln -s "$PWD/pmbootstrap/pmbootstrap.py" ~/.local/bin/pmbootstrap
$ pmbootstrap --version
$ source ~/.profile
```

## Install Hotspot on Raspberry
Tutorial:  
https://github.com/RaspAP/raspap-webgui

# Flash PostmarketOS
```bash
fastboot -s <serial_number> flash boot lk2nd.img
fastboot -s <serial_number> flash userdata fairphone-fp2.img
```