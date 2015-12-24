#!/usr/bin/python

# Genera un escaneo nmap cada cierto tiempo fijo

import time
import os

duration = 3600 # Seconds (1 hour)
interval = 300 #Seconds - 5 minutes
nmapCommand = 'nmap -A 192.168.56.100/28' # Scan from 192.168.56.96-101

iteraciones = 0

while iteraciones*interval < duration:
	os.system(nmapCommand)
	time.sleep (interval)
	

