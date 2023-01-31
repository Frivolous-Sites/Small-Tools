#!/usr/bin/env python3
# -*- coding: utf-8 -*

from os import popen
from time import sleep

t = 60
iface = "ens3"

oldRXPackets = 0
oldRXBytes = 0
oldTXPackets = 0
oldTXBytes = 0
for i in range(t):
	temp = popen("ifconfig " + iface + " | grep \"RX packets\" | sed -e 's/[^0-9]/ /g' -e 's/^ *//g' -e 's/ *$//g' | tr -s ' '").read().split(" ")
	newRXPackets = int(temp[0])
	newRXBytes = int(temp[1])
	temp = popen("ifconfig " + iface + " | grep \"TX packets\" | sed -e 's/[^0-9]/ /g' -e 's/^ *//g' -e 's/ *$//g' | tr -s ' '").read().split(" ")
	newTXPackets = int(temp[0])
	newTXBytes = int(temp[1])
	print("RX (per second): {b:6.3f} MiB {p:6d} packets".format(b = (newRXBytes - oldRXBytes) / 1024 / 1024, p = newRXPackets - oldRXPackets), end = "; ")
	print("TX (per second): {b:6.3f} MiB {p:6d} packets".format(b = (newTXBytes - oldTXBytes) / 1024 / 1024, p = newTXPackets - oldTXPackets))
	oldRXPackets = newRXPackets
	oldTXPackets = newTXPackets
	oldRXBytes = newRXBytes
	oldTXBytes = newTXBytes
	sleep(1)
