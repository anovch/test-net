#!/bin/sh

H1=192.168.40.10
H2=192.168.40.13
R1=192.168.40.11
R2=192.168.40.12

ssh root@$H1 'ip link set eth1 up'
ssh root@$H1 'ip addr add 192.168.50.10/24 dev eth1'
ssh root@$H1 'ip route add 0/0 dev eth1 via 192.168.50.1'

ssh root@$H2 'ip link set eth1 up'
ssh root@$H2 'ip addr add 192.168.51.10/24 dev eth1'
ssh root@$H2 'ip route add 0/0 dev eth1 via 192.168.51.1'

ssh root@$R1 'ip link set eth1 up'
ssh root@$R1 'ip link set eth2 up'
ssh root@$R1 'ip addr add 192.168.50.1/24 dev eth1'
ssh root@$R1 'ip addr add 172.16.1.10/12 dev eth2'
ssh root@$R1 'echo 1 > /proc/sys/net/ipv4/ip_forward'

ssh root@$R2 'ip link set eth1 up'
ssh root@$R2 'ip link set eth2 up'
ssh root@$R2 'ip addr add 192.168.51.1/24 dev eth1'
ssh root@$R2 'ip addr add 172.16.1.11/12 dev eth2'
ssh root@$R2 'echo 1 > /proc/sys/net/ipv4/ip_forward'

cp ./gre_r1.sh ../R1/mnt/home/root/gre.sh
cp ./gre_r2.sh ../R2/mnt/home/root/gre.sh

ssh root@$R1 './gre.sh'
ssh root@$R2 './gre.sh'

