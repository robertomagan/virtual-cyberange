#!/bin/bash


if [[ $EUID -ne 0 ]]; then
   echo "WARNING: Ejecute este script como root ***" 1>&2
   exit 1
fi


iptables -F INPUT
iptables -F OUTPUT
iptables -F FORWARD

# Matamos el proceso
killall nfcapd
