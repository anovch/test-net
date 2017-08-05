#!/bin/sh

tnl=tnl0
remote=172.16.1.11
local=172.16.1.10
ip=192.168.50.100
range=192.168.51.0/24
#   ip tunnel del $tnl
ip tunnel add $tnl mode gre local $local remote $remote ttl 255
ip addr add $ip dev $tnl
ip link set $tnl up
ip route add $range dev $tnl
