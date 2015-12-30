#!/usr/bin/python

# Genera un escaneo nmap cada cierto tiempo fijo

import time
import os
import argparse
import datetime

parser = argparse.ArgumentParser (description='Execute a nmap scan against a destination (network or host')
parser.add_argument(dest='destination', metavar='destination', action='store', help='IP address/segment of the victims', nargs=1)
parser.add_argument('-i', dest='interval', metavar='interval', action='store', type=int, default=300, help='interval(seconds) between the end of a scan and the start of the next scans. Default 5 min')
parser.add_argument('-d', dest='duration', metavar='duration', action='store', type=int, default=3600, help='total duration (seconds) of the scan process. Default 1h')

args = parser.parse_args()


duration = datetime.timedelta(seconds=args.duration) # Seconds (default 1 hour)
interval = args.interval #Seconds (default 5 minutes)
nmapCommand = 'sudo nmap -n -sS ' + args.destination[0]  # -n: no DNS resolution, -sS SYN Stealth scan 


inicio = datetime.datetime.now()

iteraciones = 0
while datetime.datetime.now()-inicio < duration:
	if (iteraciones != 0):
		print 'Transcurridos ' + str((datetime.datetime.now()-inicio).seconds)+ ' segundos.'
		print 'En espera durante: ' + str(interval)
		time.sleep(interval)
	
	iteraciones = iteraciones+1
	print 'Ejecutando: ' + nmapCommand
	os.system(nmapCommand)
	print '--> Ejecutado. '
	

