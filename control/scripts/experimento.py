#!/usr/bin/python
# -*- coding: cp1252 -*-

# Autor: Gabriel Maciá
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

LOGFILENAME = 'DoS_attack.log'
LOGLEVEL = logging.DEBUG
LOGDIR = '../log/'

# El formato de la lista de comandos es: [tInicio, comando]
lista_comandos = [
                  [1, 'ssh gmacia@192.168.56.104 echo prueba1'], #Comentario para la ejecución
                  [1, 'ssh gmacia@192.168.56.104 echo prueba2'],
                  [2, 'hostname; date']              
                  
                  
                  ]

comandos_procesado = [
                      
                      ]


##########################################







def execute_command (instanteEjecucion, command):
    
    time.sleep(instanteEjecucion)
    tInicial = time.strftime('%X')
    beginInterval= datetime.datetime.now()
    output = subprocess.check_output(command, shell=True).decode('utf-8')
    tFinal = time.strftime('%X')
    endInterval = datetime.datetime.now()
    interval = endInterval - beginInterval
     
    cabecera = ('   -->(result)$ ' + 
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
    
 

if __name__ == '__main__':

    #global lista_comandos
    logging.basicConfig(
                        #filename=LOGDIR + time.strftime('%y%m%d_%H.%M.%S_')+ LOGFILENAME,
                        level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
                        )
    log = logging.getLogger("MSNM_main")

    # Ejecución de los comandos cada uno en un thread
    
    log.info ('[+] Inicio de ejecución de comandos')
    threads = []
    for twait, command in lista_comandos: 
        t = Thread(target=execute_command, args=(twait, command,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


    log.info ('[+] Inicio de procesado: ' + time.strftime('%X %d/%m/%y'))

    for command in comandos_procesado:
        execute_command(0, command)

    log.info ('[+] Final de procesado: ' + time.strftime('%X %d/%m/%y'))    