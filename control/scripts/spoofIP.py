#!/usr/bin/python
# -*- coding: cp1252 -*-

# Autor: Gabriel MaciÃ¡
# Fecha: 14/12/2015

# Script para cambiar las IPs de los nodos por IPs del rango
# 192.168.56.x, donde solo puede haber 3 IPs en el rango escaneado: 
# 
# 192.168.56.100/28 = 192.168.56.96 - 192.168.56.111
# 
# y debe haber 100 IPs diferentes.
# La IP 192.168.56.102 es la del servidor. 

import random
import sys
import argparse
import datetime


parser = argparse.ArgumentParser (description='Spoof a origin IP to destination IPs in a given range')
parser.add_argument('-s', dest='atacante_ip', metavar='atacante_ip', action='store', help='IP address of the victim', nargs=1)
parser.add_argument('-t', dest='type', metavar='type', action='store', default='public', choices=['private', 'public'], help='public/private. default: public')
parser.add_argument('--orig_csv', dest='dump_original', metavar='dump_original', action='store', help='Fichero dump original (formato CSV).')
parser.add_argument('--dest_csv', dest='dump_destino', metavar='dump_destino', action='store', help='Fichero dump destino (formato CSV).')
args = parser.parse_args()



def generaListaIpsPrivadas (size): #Size es el tamaño de la lista

	rangoPrivadas = '192.168.31.'
	listaIpsPrivadas = []

	i=0
	while i < size:

		random.seed(datetime.datetime.now()) 
		prefijo = random.randint(1,254)
		if (prefijo <96 or prefijo >111):
			ip = rangoPrivadas + str(prefijo)
			if ip not in listaIpsPrivadas:
				listaIpsPrivadas.append(ip)
				i += 1
 
	return listaIpsPrivadas

def generaListaIpsPublicas ():
	listaIpsPublicas = []
	i = 0
	while i<1000: #Creamos una lista con 1000 direcciones IP aleatorias
		b1 = random.randint(1,254)
		b2 = random.randint(1,254)
		b3 = random.randint(1,254)
		b4 = random.randint(1,254)
		listaIpsPublicas.append(str(b1)+'.'+str(b2)+'.'+str(b3)+'.'+str(b4))
		i = i+1
	return listaIpsPublicas


DUMP_MODIFICADO = args.dump_destino
DUMP_ORIGINAL = args.dump_original
IP_ATACANTE = args.atacante_ip[0]

#print "ip: " + IP_ATACANTE
#print "fin: " + DUMP_ORIGINAL

if args.type == 'private':
	listaIps = generaListaIpsPrivadas(120)
else: 
	listaIps = generaListaIpsPublicas()

with open (DUMP_MODIFICADO, "w") as fout:
	with open (DUMP_ORIGINAL, "r") as fin:
		for line in fin:
			cad = line.split(',')
			if cad[5] != '4444' and cad[6] != '4444':
				if cad[3] == IP_ATACANTE:
					cad[3] = random.choice(listaIps)
				if cad[4] == IP_ATACANTE:
					cad[4] = random.choice(listaIps)

			fout.write(','.join(cad))
			
print 'Output generado en: ' + DUMP_MODIFICADO	
