#!/usr/bin/python
# -*- coding: cp1252 -*-

# Autor: Gabriel Maciá
# Fecha: 23/12/2015


import time
from random import randint
import sys


if __name__ == '__main__':
	
	try: 
		while True: 
			time.sleep (randint(1,4))
			length = randint(1, 10000)
			print str(length) + ': ' + 'A' * length

	except IOError as e: 
		print >> sys.stderr, 'Error en la conexion: ' + str(e)