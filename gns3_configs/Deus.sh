#!/bin/sh
sysctl -w net.ipv4.ip_forward=1

ip addr flush dev eth0
ip addr add 10.82.19.46/30 dev eth0
ip link set eth0 up

ip addr flush dev eth1
ip addr add 10.82.18.1/25 dev eth1
ip link set eth1 up

ip addr flush dev eth2
ip addr add 10.82.19.49/30 dev eth2
ip link set eth2 up

ip route add default via 10.82.19.45

ip route add 10.82.18.128/25 via 10.82.19.50
ip route add 10.82.19.0/26 via 10.82.19.50
ip route add 10.82.19.40/30 via 10.82.19.45
