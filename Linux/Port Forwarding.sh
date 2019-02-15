#!/bin/bash

IPTBL=/sbin/iptables

IF_IN=[your_eth_I/F]
PORT_IN=[desired_port]

IP_OUT=[dest_ip]
PORT_OUT=[dest_port]

echo "1" > /proc/sys/net/ipv4/ip_forward
$IPTBL -A PREROUTING -t nat -i $IF_IN -p tcp --dport $PORT_IN -j DNAT --to-destination ${IP_OUT}:${PORT_OUT}
$IPTBL -A FORWARD -p tcp -d $IP_OUT --dport $PORT_OUT -j ACCEPT
#$IPTBL -A POSTROUTING -t nat -j MASQUERADE
