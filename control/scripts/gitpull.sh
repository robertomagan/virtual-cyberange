#!/bin/bash

# Este script realiza un git pull en el directorio ~/git/VERITASExperimentalScripts
# de todas las maquinas en la lista de maquinas de VERITAS


maquinas=(atacante borderRouter routerR1 routerR2 routerR3 m1.2 m2.2 m3.2 dmz wwwserver)
DIR='git/VERITASExperimentalScripts'



for m in ${maquinas[*]}
do
	printf "[+] Connecting to: %s\n" $m
	eval $(printf "ssh nesg@%s \"cd %s; git pull\"\n" $m $DIR)
done
