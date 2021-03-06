#!/usr/bin/python
# -*- coding: cp1252 -*-

# Autor: Gabriel Maci?
# Fecha: 14/12/2015

import sys
import logging
import argparse
import time
import datetime
import subprocess
from threading import Thread

##########################################
# DEFINICION DE VARIABLES Y CONSTANTES
##########################################

#LOGFILENAME = 'DoS_attack.log'
#LOGLEVEL = logging.DEBUG
LOGDIR = '../log/'

def cadena_color (cadena, color):

	if (color != "rojo" and color != "verde"):
		color = "rojo"

	escape = '\x1B['
	rojo = '31m'
	verde = '32m'
	reset = escape + '0m'

	if color == "rojo":
		color = rojo
	if color == "verde":
		color = verde

	
	return escape + color + cadena + reset
	

class VeritasExperiment:

	def __init__(self, experimentName="veritasExperiment"):
		self.comandosEjecucion = []
		self.comandosProcesado = []
		self.experimentName = experimentName
		logging.basicConfig(
                        #filename=LOGDIR + experimentName + time.strftime('.%y%m%d%H%M%S') + '.log',
                        level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
                        )
		self.log = logging.getLogger(experimentName)


	def esComando (self, comando):
		# Comprueba si el comando tiene el formato correcto
		if isinstance (comando, list) and isinstance(comando[0],int) and isinstance(comando[1],str):
			return True
		else:
			return False

	def insertaListaComandosEjecucion (self, listaComandos):
		if isinstance(listaComandos, list):
			for comando in listaComandos:
				self.insertaComandoEjecucion(comando)

	def insertaListaComandosProcesado (self, listaComandos):
		if isinstance(listaComandos, list):
			for comando in listaComandos:
				self.insertaComandoProcesado(comando)

	def insertaComandoEjecucion (self, comando):
		if self.esComando(comando):
			if comando[0]<0:
				comando[0] = 0
			self.comandosEjecucion.append(comando)
			self.ordenaListaComandos (self.comandosEjecucion)
		
		else:
			print 'Comando no insertado por error: ' + str(comando)
	
	def insertaComandoProcesado (self, comando):
		# Comprueba si el comando tiene el formato correcto
		if self.esComando(comando):
			if comando[0]<0:
				comando[0] = 0
			self.comandosProcesado.append(comando)
			self.ordenaListaComandos (self.comandosProcesado)

		else:
			print 'Comando no insertado por error: ' + str(comando)

		
	def ordenaListaComandos(self, lista): 
		lista.sort(key=lambda x: x[0])
		
	def imprimeComandos (self):
		print '------------------------------------'
		print 'Lista de comandos de ejecucion:'
		for comando in self.comandosEjecucion:
			print "t=" + str(comando[0]) + "s\t" + str(comando[1])
		print '\nLista de comandos de procesado:'
		for comando in self.comandosProcesado:
			print "t=" + str(comando[0]) + "s\t" + str(comando[1])
		print '------------------------------------\n'


	def executeCommand (self, instanteEjecucion, command, n):
		
		log = self.log
		
		time.sleep(instanteEjecucion)
		tInicial = time.strftime('%X')
		beginInterval= datetime.datetime.now()
		
		cabecera = (cadena_color('   -->(execute[' + str(n) + '])$ ', "rojo") + 
				  command +
				  ' (' +
				  tInicial +
				  ')'
				  )		
		log.info(cabecera)
				
		try:
			output = subprocess.check_output(command, shell=True).decode('utf-8')
		
		except Exception as e:
			output = "Error. Excepcion recibida en proceso: " + str(e)
		
		tFinal = time.strftime('%X')
		endInterval = datetime.datetime.now()
		interval = endInterval - beginInterval
		 
		cabecera = (cadena_color('   -->(result[' + str(n) + '])$ ',"verde") + 
				  command +
				  ' (' +
				  str(interval.seconds/3600)+'d'+str(interval.seconds%3600/60)+'m'+str(interval.seconds%60)+'s' + 
				  '---' + 
				  tInicial +
				  '-' + 
				  tFinal + 
				  ')'
				  )

		log.info (cabecera + '\n\t\t\t\t\t\t\t|' + output.strip().replace('\n','\n\t\t\t\t\t\t\t|'))

		
	 

	def execute (self):



		# Ejecuci?n de los comandos cada uno en un thread
		log = self.log
		
		log.info ('#################################################\n\t\t\t\t\t\t[+] Inicio de ejecucion de comandos\n\t\t\t\t\t\t#################################################')
		threads = []
		n = 1 # Numero de indice que identificara al comando ejecutado
		
		for twait, command in self.comandosEjecucion: 
			t = Thread(target=self.executeCommand, args=(twait, command, n))
			n = n+1
			threads.append(t)
			t.start()

		for t in threads:
			t.join()

		log.info ('#################################################\n\t\t\t\t\t\t[+] Inicio de procesado: ' + time.strftime('%X %d/%m/%y') + '\n\t\t\t\t\t\t#################################################')

#		log.info ('[+] Inicio de procesado: ' + time.strftime('%X %d/%m/%y'))

		for comando in self.comandosProcesado:
			self.executeCommand(0, comando[1], n)
			n = n+1

		log.info ('[+] Final de procesado: ' + time.strftime('%X %d/%m/%y'))    


if __name__ == '__main__':
	
	exp = VeritasExperiment() 
