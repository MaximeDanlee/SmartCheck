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

## Linux
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

# Librairy to add Fairphone 
```bash
sudo apk add stress-ng
```