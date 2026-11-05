#!/bin/sh
sysctl -w net.ipv4.ip_forward=1

ip addr flush dev eth0
ip addr add 10.82.24.130/30 dev eth0
ip link set eth0 up

ip addr flush dev eth1
ip addr add 10.82.10.81/29 dev eth1
ip link set eth1 up

ip addr flush dev eth2
ip addr add 10.82.19.41/30 dev eth2
ip link set eth2 up

ip addr flush dev eth3
ip addr add 10.82.22.65/30 dev eth3
ip link set eth3 up

ip route add default via 10.82.24.129

ip route add 10.82.0.0/22 via 10.82.10.82
ip route add 10.82.4.0/22 via 10.82.10.84
ip route add 10.82.8.0/22 via 10.82.10.83
ip route add 10.82.10.64/28 via 10.82.10.84
ip route add 10.82.16.0/22 via 10.82.19.42
ip route add 10.82.20.0/22 via 10.82.22.66

sysctl -w net.ipv4.conf.all.send_redirects=0
sysctl -w net.ipv4.conf.eth1.send_redirects=0
