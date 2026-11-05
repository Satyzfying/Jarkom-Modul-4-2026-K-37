#!/bin/sh
sysctl -w net.ipv4.ip_forward=1

ip addr flush dev eth0
ip addr add 192.168.122.50/24 dev eth0
ip link set eth0 up

ip route add default via 192.168.122.1

ip addr flush dev eth1
ip addr add 10.82.24.1/25 dev eth1
ip link set eth1 up

ip addr flush dev eth2
ip addr add 10.82.24.129/30 dev eth2
ip link set eth2 up

ip route add 10.82.0.0/19 via 10.82.24.130

iptables -t nat -F POSTROUTING
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
echo 'nameserver 8.8.8.8' > /etc/resolv.conf
