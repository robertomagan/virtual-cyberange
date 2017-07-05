#!/usr/bin/python
# -*- coding: cp1252 -*-

# Autor: Gabriel Macia
# Fecha: 14/12/2015

# realiz spoofing de direcciones IP. 
# Asume que el fichero nfdump no viene agregado por IPs/Puertos (no se genera con opciones -a, -b o -B)

import random
import sys
import argparse
import datetime
import os
from __builtin__ import file
from _smbc import File





def generaListaIpsPrivadas (size, rango): #Size es el tamaño de la lista

	rangoPrivadas = rango
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

def generaListaIpsPublicas (size):
	listaIpsPublicas = []
	i = 0
	while i<size: #Creamos una lista con 1000 direcciones IP aleatorias
		b1 = random.randint(1,254)
		b2 = random.randint(1,254)
		b3 = random.randint(1,254)
		b4 = random.randint(1,254)
		listaIpsPublicas.append(str(b1)+'.'+str(b2)+'.'+str(b3)+'.'+str(b4))
		i = i+1
	return listaIpsPublicas

if __name__ == '__main__':



	parser = argparse.ArgumentParser (description='Spoof a origin IP to destination IPs in a given range')
	parser.add_argument('-s', dest='atacante_ip', metavar='atacante_ip', action='store', help='IP address of the victim', nargs=1)
	parser.add_argument('-n', dest='numberIps', metavar='numberIps', type=int, action='store', help='# of different IPs in the spoofing list')
	parser.add_argument('-t', dest='type', metavar='type', action='store', default='public', choices=['private', 'public'], help='public/private. default: public')
	parser.add_argument('-f', dest='dump_file', metavar='dump_file', action='store', help='Fichero dump original (formato CSV).')
	parser.add_argument('-r', dest='rango_privadas', metavar='rango_privadas', action='store', help='Rango de direcciones para spoofing')
	#parser.add_argument('--dest_csv', dest='dump_destino', metavar='dump_destino', action='store', help='Fichero dump destino (formato CSV).')
	args = parser.parse_args()

	file = args.dump_file + '.spoof.csv'
	DUMP_MODIFICADO = file
	if (os.path.exists(file)):
		os.system ('cp ' + file + ' dump.tmp')
		DUMP_ORIGINAL = 'dump.tmp'
	else: 
		DUMP_ORIGINAL = args.dump_file + '.csv'
	
#	print 'Original: ' + DUMP_ORIGINAL
#	print 'Modificado: ' + DUMP_MODIFICADO
#	exit()
	#DUMP_MODIFICADO = args.dump_destino
	#DUMP_ORIGINAL = args.dump_original
	
	IP_ATACANTE = args.atacante_ip[0]
	rango = args.rango_privadas
	if rango == None:
		rango = "Any"
	print "Spoofing " + IP_ATACANTE + " with " + str(args.numberIps) + " " + args.type + " addresses. Rango: " + rango + ". File: " + DUMP_ORIGINAL
	
	

	lista_ips_modificadas = []  # Usamos la lista para almacenar el cambio en un sentido y mantenerlo en el flujo de vuelta
								# La lista contiene [['ip', puerto_src, puerto_dst], 'ip_spoof', [...], 'ip_spoof2']
	size = args.numberIps	
	if args.type == 'private':
		listaIps = generaListaIpsPrivadas(size, args.rango_privadas)
	else: 
		listaIps = generaListaIpsPublicas(size)
	
	with open (DUMP_MODIFICADO, "w") as fout:

		
		with open (DUMP_ORIGINAL, "r") as fin:
			vacio = (os.path.getsize(DUMP_ORIGINAL)==0)
			for line in fin:
				if line == 'No matched flows\n' or vacio:
					print "[-] Fichero vacio: " + DUMP_ORIGINAL
					sys.exit()

				cad = line.split(',')
				if cad[5] != '4444' and cad[6] != '4444':
					#print line
					if cad[3] == IP_ATACANTE:
						#print 'Encontrada cad[3]'
						tupla = [cad[4],cad[5],cad[6]]
						if tupla in lista_ips_modificadas:
							indice = lista_ips_modificadas.index(tupla)
							cad[3] = lista_ips_modificadas[indice+1]
							# Elimina la tupla de la lista de ips modificadas
							lista_ips_modificadas = lista_ips_modificadas[:indice] + lista_ips_modificadas[indice+2:]
							#print "Encontrada tupla y eliminada: " + str(tupla)
						
						else:
							cad[3] = random.choice(listaIps)
							#Inserta la nueva tupla
							lista_ips_modificadas.append(tupla)
							lista_ips_modificadas.append(cad[3])
							#print "Insertada tupla: " + str(lista_ips_modificadas)
							
					if cad[4] == IP_ATACANTE:
						#print 'Encontrada cad[4]'
						tupla = [cad[3],cad[6],cad[5]] # Notar que cambiamos el orden de los puertos
						if tupla in lista_ips_modificadas:
							indice = lista_ips_modificadas.index(tupla)
							cad[4] = lista_ips_modificadas[indice+1]
							# Elimina la tupla de la lista de ips modificadas
							lista_ips_modificadas = lista_ips_modificadas[:indice] + lista_ips_modificadas[indice+2:]
							#print "Encontrada tupla y eliminada: " + str(tupla)
						
						else:
							cad[4] = random.choice(listaIps)
							#Inserta la nueva tupla
							lista_ips_modificadas.append(tupla)
							lista_ips_modificadas.append(cad[4])
							#print "Insertada tupla: " + str(lista_ips_modificadas)	
				fout.write(','.join(cad))
				
	print 'Output generado en: ' + DUMP_MODIFICADO	
	os.system ('rm -f dump.tmp')