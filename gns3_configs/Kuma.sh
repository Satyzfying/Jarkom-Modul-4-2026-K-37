#!/bin/sh
ip addr flush dev eth0
ip addr add 10.82.21.4/24 dev eth0
ip link set eth0 up

ip route add default via 10.82.21.1
echo 'nameserver 8.8.8.8' > /etc/resolv.conf
