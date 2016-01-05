#!/bin/bash

COLECTOR_DIR='/home/nesg/git/VERITASExperimentalScripts/machines/routers/capturas'
HOSTNAME=`hostname`

if [[ $EUID -ne 0 ]]; then
   echo "WARNING: Ejecute este script como root ***" 1>&2
   exit 1
fi

echo "[+] Desactivando configuracion anterior si esta activa..."
./deactivateNetflow.sh



echo "[+] Activando el modulo ipt_netflow, con destino 127.0.0.1:12345"
modprobe ipt_NETFLOW destination=127.0.0.1:12345

#echo "Hecho"
echo "[+] Insertando reglas en cortafuegos"

# Solo insertamos en la regla FORWARD porque solo estamos interesados en el tráfico que se intercambian los nodos  de la red
# No metemos regla en INPUT y OUTPUT porque se supone que no queremos registrar los traficos de gestion del router

iptables -I FORWARD -i eth1 -j NETFLOW
iptables -I FORWARD -i eth2 -j NETFLOW

#echo "Hecho"
# iptables -L -n

#echo
echo [+] Activando el colector con el comando: nfcapd -w -D -t 600 -l $COLECTOR_DIR -I $HOSTNAME -p 12345

nfcapd -w -D -t 600 -l $COLECTOR_DIR -I $HOSTNAME -p 12345
