#!/bin/bash

# Este script busca en el directorio $DIR los archivos que se llamen nfcapd.<fecha> y los renombra a nfcapd_hostname.<fecha>


HOSTNAME=`hostname`
DIR='../capturas/'

# Inicio de script

FILES_ORIG="$(ls $DIR |grep -v -e $HOSTNAME | grep nfcapd)"

echo [+] Renombrando ficheros en directorio $DIR con nombre de host: $HOSTNAME

cd $DIR

for i in $FILES_ORIG 
do
  eval $(echo $i|awk -v hostname=$HOSTNAME '{printf "echo %s -- %s\n", $0, "nfcapd_" hostname substr($0,7)}')
  eval $(echo $i|awk -v hostname=$HOSTNAME '{printf "mv %s %s\n", $0, "nfcapd_" hostname substr($0,7)}')
done
