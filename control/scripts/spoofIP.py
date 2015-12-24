#!/usr/bin/python
# -*- coding: cp1252 -*-

# Autor: Gabriel Maciá
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

IP_ATACANTE_SPOOF_PUBLICAS = '192.168.56.5'
IP_ATACANTE_SPOOF_PRIVADAS = '192.168.56.4'
IP_CLIENTES = '192.168.56.103'
IP_SERVIDOR = '192.168.56.104'


def generaListaIpsPrivadas ():
	listaIpsPrivadas = []

	i=0
	while i < 97:

		prefijo = random.randint(1,254)
		if (prefijo <96 or prefijo >111):
			ip = '192.168.56.' + str(prefijo)
			if ip not in listaIpsPrivadas:
				listaIpsPrivadas.append(ip)
				i += 1

	# Al final anado tres del rango
	listaIpsPrivadas += ['192.168.56.103', '192.168.56.105', '192.168.56.100']
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

#main

if len(sys.argv)<3:
	print "Uso: ./cambiaIP.py dumpOriginal.csv dumpFinal.csv"
	exit(0)


DUMP_MODIFICADO = sys.argv[2]
DUMP_ORIGINAL = sys.argv[1]


listaIpsPrivadas = generaListaIpsPrivadas()
listaIpsPublicas = generaListaIpsPublicas()

with open (DUMP_MODIFICADO, "w") as fout:
	with open (DUMP_ORIGINAL, "r") as fin:
		for line in fin:
			cad = line.split(',')
			if cad[5] != '4444' and cad[6] != '4444':
				if cad[3] == IP_ATACANTE_SPOOF_PRIVADAS or cad[3] == IP_CLIENTES:
					cad[3] = random.choice(listaIpsPrivadas)
				if cad[4] == IP_ATACANTE_SPOOF_PRIVADAS or cad[4] == IP_CLIENTES:
					cad[4] = random.choice(listaIpsPrivadas)
				if cad[3] == IP_ATACANTE_SPOOF_PUBLICAS:
					cad[3] = random.choice(listaIpsPrivadas)
				if cad[4] == IP_ATACANTE_SPOOF_PUBLICAS:
					cad[4] = random.choice(listaIpsPrivadas)
				
			
			fout.write(','.join(cad))
			
print 'Output generado en: ' + DUMP_MODIFICADO	
