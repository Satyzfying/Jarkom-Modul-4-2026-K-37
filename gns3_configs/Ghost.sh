#!/bin/sh
ip addr flush dev eth0
ip addr add 10.82.16.3/23 dev eth0
ip link set eth0 up

ip route add default via 10.82.16.1
echo 'nameserver 8.8.8.8' > /etc/resolv.conf
