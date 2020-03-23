#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
from datetime import datetime
from re import findall
from secrets import token_hex

currentTime = datetime.today()
timeString = str(currentTime.strftime('%Y%m%d'))

baseDir = "zones/"
subDir=[]
subDir = [f for f in sorted(os.listdir(baseDir))]

for sub_dir in subDir:
	for zoneFile in os.listdir(baseDir + sub_dir):
		if zoneFile.endswith(".db"):
			with open(baseDir + sub_dir + "/" + zoneFile, 'r') as zone_file:
				zoneData = zone_file.readlines()
				zoneSerials = findall(r'\b\d{10}\b', zoneData[9])
				zoneSerial = str(zoneSerials[0])
				if zoneSerial[:8] == timeString:
					serialSerial = str(int(zoneSerial[-2:]) + 1).zfill(2)
					newSerial = timeString + serialSerial
				else:
					newSerial = timeString + "00"
				zoneData[9] = zoneData[9].replace(zoneSerial, newSerial)
			with open(baseDir + sub_dir + "/" + zoneFile, 'w') as zone_file:
				zone_file.writelines(zoneData)
			os.chdir(baseDir + sub_dir)
			os.system('dnssec-signzone -A -3 ' + str(token_hex(8)).upper() + ' -N INCREMENT -o ' + sub_dir + ' -t ' + zoneFile)
			os.chdir('../../')

# Before you start,
# please make sure that your zone file ends with ".db" and placed under the directory which name is the domain itself.
# For example, if this file is placed in /etc/bind;
# zone.db file should be placed in /etc/bind/example.com/zone.db

# Following commands may help when you generate keys:
# dnssec-keygen -a ECDSAP256SHA256 -n ZONE example.com
# dnssec-keygen -f KSK -a ECDSAP256SHA256 -n ZONE example.com
