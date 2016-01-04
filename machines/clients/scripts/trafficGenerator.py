#!/usr/bin/python

# Autor: Gabriel Macia
# Fecha: 14/12/2015

# Uso: trafficGenerator -n <NumeroClientes> -t <TiempoSimulacionSegundos>
# Programa para ejecutar una simulacion de varios clientes haciendo peticiones
# http a un servidor <destino>. Ver README.md para detalles sobre el proyecto httpTrafficGenerator
# que se ha utilizado aqui. (El comando de ejecucion que se lanza desde este script es 'java traffic'

import time
from threading import Thread, currentThread
import random
import os
from optparse import OptionParser
import logging 
import fileinput

##########################################
# DEFINICION DE VARIABLES Y CONSTANTES
##########################################
RUTA_HTTPTRAFFICGENERATOR = '../httpTrafficGenerator/'

LOGFILENAME = 'trafficGenerator.log'
LOGLEVEL = logging.DEBUG
LOGDIR = '../log/'

##########################################


def request(i):
	global tSimulation
	
	startTime = time.time()
	endTime = startTime + tSimulation
	
	log.debug( 'Cliente (' + str(i) + ') Generando trafico durante ' + str(tSimulation) + ' segundos')
	
	while time.time()<endTime:
		interval = random.expovariate(0.025)   #Exponencial de media de 40 segundos entre peticion web 1/40
		#interval = random.expovariate(0.java 2)   #Exponencial de media de 5 segundos entre peticion web 1/5
		interval = random.expovariate(3)   #Exponencial de media de 5 segundos entre peticion web 1/5

		log.debug('Peticion de cliente (' + str(i) + ') en ' + str(interval) + ' segundos')
		time.sleep (interval) 
		os.system('cd ' + RUTA_HTTPTRAFFICGENERATOR + '; java traffic')
 

	
	
##########################################
# Main 
##########################################


if __name__ == '__main__':


	logging.basicConfig(
						filename=LOGDIR + time.strftime('%y%m%d_%H.%M.%S_')+ LOGFILENAME,
						level=logging.DEBUG,
						format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
						)
	log = logging.getLogger("httpTrafficGenerator")

	parser = OptionParser()
	parser.add_option('-n', default=1, type='int', dest = 'clients', help='Number of clients to make requests')
	parser.add_option('-t', default=1, type='int', dest = 'time', help='duration of the traffic (seconds)')
	parser.add_option('-d', default='10.0.0.1', dest = 'webserver', help='IP of the destination web server')

	(options, args) = parser.parse_args()
	tSimulation = options.time
	
	log.info ('Inicio a las: ' + time.strftime('%X %d/%m/%y'))

	print 'Generating traffic to ' + options.webserver
	print '--------------------------------------------'
	print 'Simulation time: ' + str(tSimulation) + ' seconds'
	print 'Number of simultaneous clients: ' + str(options.clients)
	print '--------------------------------------------'


	# Esto reemplaza la linea en el fichero servers.txt en la que aparece webserver
	# por la IP del webserver indicado como destino en las opciones.
	for line in fileinput.input('../httpTrafficGenerator/servers.txt', inplace=True):
		l=line.strip().split()
		if l[0]=='webserver':
			l[1] = options.webserver + ':80'
		print '\t'.join(c for c in l)


	# A thread is started for every connection to the server. Note that every connection could get n URLs in a persistent connection
	threads = []
	for i in range (options.clients):
		t = Thread(target=request, args=(i,))
		threads.append(t)
		t.start()

	for t in threads:
		t.join()

	log.info ('Finalizado a las: ' + time.strftime('%X %d/%m/%y'))

