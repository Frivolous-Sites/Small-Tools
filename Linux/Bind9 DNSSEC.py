#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os, sys
from datetime import datetime
from re import findall, match
from secrets import token_hex

if sys.argv[1] == "-d":
	GeoIP_Countries = ["US"]
	with open('GeoIP.acl', 'r') as zone_file:
		zoneData = zone_file.readlines()
		for i in range(len(zoneData)):
			if match(r'[ \t]', zoneData[i]):
				zoneData[i] = '\tecs ' + zoneData[i].lstrip()
			elif zoneData[i].startswith('acl'):
				if zoneData[i][4:6] in GeoIP_Countries:
					zoneData[i] = 'acl "ecs_' + zoneData[i][4:6] + '" {\n\tkey Transfer_' + zoneData[i][4:6] + ';\n'
				else:
					zoneData[i] = 'acl "ecs_' + zoneData[i][4:6] + '" {\n'

	with open('ecs_GeoIP.acl', 'w') as zone_file:
		zone_file.writelines(zoneData)

# Above code generates GeoIP acl which supports ecs (EDNS Client-Subnet).
# Assuming the original file is GeoIP.acl (https://geoip.site/), we are going to create ecs_GeoIP.acl

# `GeoIP_Countries` list includes countries that are not in default view.
# This script assumes that you are using key auth between masters and slaves.
# The key has "Transfer_XX" name (e.g., Transfer_US)
# Therefore, if the country is in `GeoIP_Countries` list, its acl block will include the key file (aka, key Transfer_US;).
# Generate key: dnssec-keygen -a HMAC-SHA512 -b 512 -n HOST -r /dev/urandom Transfer_XX
# Key config:
#key "Transfer_XX" {
#algorithm HMAC-SHA512;
#secret "CONTENT_IN_Ktransfer_xx.*.private";
#};

else:
	currentTime = datetime.today()
	timeString = str(currentTime.strftime('%Y%m%d'))

	os.chdir('/etc/bind')
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
