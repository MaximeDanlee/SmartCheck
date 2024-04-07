# Connect via SSH
```bash
ssh pptc@172.16.42.1
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
xorg aussi

```

ajouter :

sudo nano /etc/ssh/sshd_config
X11Forwarding yes


# Package to add  on Raspberry
```bash
sudo apt-get -y install hostapd dnsmasq
```

# Hotspot on Raspberry
Tutorial:  
https://github.com/RaspAP/raspap-webgui

# Flash PostmarketOS
```bash
fastboot -s <serial_number> flash boot lk2nd.img
fastboot -s <serial_number> flash userdata fairphone-fp2.img
```