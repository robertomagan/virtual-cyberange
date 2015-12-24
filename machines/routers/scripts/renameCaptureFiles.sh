#!/bin/bash

HOSTNAME=`hostname`
DIR='../capturas/'
FILES_ORIG='nfcapd*'

echo [+] Renombrando ficheros en directorio $DIR con nombre de host: $HOSTNAME

cd $DIR

for i in $FILES_ORIG 
do
  eval $(echo $i|awk -v hostname=$HOSTNAME '{printf "echo %s -- %s\n", $0, "nfcapd_" hostname substr($0,7)}')
  eval $(echo $i|awk -v hostname=$HOSTNAME '{printf "mv %s %s\n", $0, "nfcapd_" hostname substr($0,7)}')
done
