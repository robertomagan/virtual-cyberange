#!/bin/bash

# Este script realiza un git pull en el directorio ~/git/VERITASExperimentalScripts
# de todas las maquinas en la lista de maquinas de VERITAS


maquinas=(borderRouter routerR1 routerR2 routerR3)
DIR='git/VERITASExperimentalScripts'



for m in ${maquinas[*]}
do
	printf "[+] Connecting to: %s\n" $m
	eval $(printf "ssh nesg@%s \"cd %s; git pull\"\n" $m $DIR)
done
