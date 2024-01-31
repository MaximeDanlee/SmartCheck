# Internet over USB PostMarketOS
## On the PostMarketOS phone
```bash
ip route add default via 172.16.42.2 dev usb0
echo nameserver 1.1.1.1 > /etc/resolv.conf
```

If the last command doesn't work you can do it manually with nano:
```bash
nano /etc/resolv.conf
```

## Linux
First, enable IP forwarding:
```bash
sysctl net.ipv4.ip_forward=1
```
iptables (Ubuntu/Arch/Alpine)
```bash
iptables -A FORWARD -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

iptables -A FORWARD -s 172.16.42.0/24 -j ACCEPT

iptables -A POSTROUTING -t nat -j MASQUERADE -s 172.16.42.0/24

iptables-save #Save changes
```
## MacOS
```bash
sudo nano /etc/sysctl.conf
```

Add this line at the end of the file

```bash
net.inet.ip.forwarding=1
```

Reload the configuration
```bash
sudo sysctl -w net.inet.ip.forwarding=1
```

