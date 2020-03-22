Procedure: 
1. Establish IPIP Tunnel;
2. Forward requests.

Scenario: 
SERVER_A has IP addresses 999.999.999.998 and 999.999.999.999 (both IP addresses are reachable)
Wants to assign 999.999.999.999 to SERVER_B
SERVER_B has public IP address 555.555.555.555

We are going to establish an IPIP tunnel between these two servers.
For the IPIP tunnel, we are going to use 192.168.192.104/30
192.168.192.105 on SERVER_A and 192.168.192.106 on SERVER_B

SERVER_A:

#!/usr/bin/env bash

iptunnel add IPnIP_1 mode ipip local 999.999.999.999 remote 555.555.555.555 ttl 255
ip addr add 192.168.192.105/30 dev IPnIP_1
ip link set IPnIP_1 up

iptables -t nat -A POSTROUTING -s 192.168.192.104/30 -j SNAT --to-source 999.999.999.999
iptables -t nat -A PREROUTING -d 999.999.999.999 -j DNAT --to-destination 192.168.192.106
iptables -A FORWARD -d 192.168.192.106 -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT

SERVER_B:

#!/usr/bin/env bash

iptunnel add IPnIP_1 mode ipip local 555.555.555.555 remote 999.999.999.999 ttl 255
ip addr add 192.168.192.106/30 dev IPnIP_1
ip link set IPnIP_1 up

echo '100 IPNIP_1' >> /etc/iproute2/rt_tables
ip rule add from 192.168.192.104/30 table IPNIP_1
ip route add default via 192.168.192.105 table IPNIP_1
