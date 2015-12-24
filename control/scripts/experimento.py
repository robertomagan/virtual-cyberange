#!/usr/bin/python
# -*- coding: cp1252 -*-

# Autor: Gabriel Maciá
# Fecha: 23/12/2015


from lib.VeritasExperiment import VeritasExperiment


##########################################
# El formato de la lista de comandos es: [tInicio, comando]

TRAFFIC_GENERATOR = 'cd git/VERITASExperimentalScripts/machines/clients/scripts/; ./trafficGenerator.py '

lista_comandos = [
                  [4, 'ssh nesg@routerR1 "echo prueba1"'], #Comentario para la ejecución
                  [1, 'ssh nesg@routerR2 "hostname; sleep 2; echo prueba2"'],
                  [2, 'hostname; date']              
                  
                  
                  ]

comandos_procesado = [
                      
                      ]


httpTraffic = [ [0, 'echo "Inicio de comandos de preprocesado (limpieza y demas)"'],
				[1, 'ssh nesg@m1.2 "' + TRAFFIC_GENERATOR + ' -n 10 -t 5 > tmp.txt"'],
				[3, 'ssh nesg@m2.2 "' + TRAFFIC_GENERATOR + ' -n 10 -t 5"']
				
				]	


##########################################


if __name__ == '__main__':
	
	e = VeritasExperiment ("experimentoPrueba")

	e.insertaComandoEjecucion([5, "ls"])
	e.insertaListaComandosEjecucion(httpTraffic)
	e.imprimeComandos()
	e.execute()
