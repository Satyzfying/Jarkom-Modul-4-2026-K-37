#!/bin/sh
sysctl -w net.ipv4.ip_forward=1

ip addr flush dev eth0
ip addr add 10.82.19.54/30 dev eth0
ip link set eth0 up

ip addr flush dev eth1
ip addr add 10.82.19.33/29 dev eth1
ip link set eth1 up

ip addr flush dev eth2
ip addr add 10.82.19.57/30 dev eth2
ip link set eth2 up

ip route add default via 10.82.19.53

ip route add 10.82.18.192/26 via 10.82.19.58
ip route add 10.82.19.0/27 via 10.82.19.58
ip route add 10.82.19.60/30 via 10.82.19.58
