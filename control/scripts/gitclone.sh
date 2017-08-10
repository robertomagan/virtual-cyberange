#!/bin/bash

# Este script realiza un git clone recursivo en el directorio ~/git/ para una rama en concreto
# de todas las maquinas en la lista de maquinas de VERITAS

if [ "$#" -ne 1 ]; then
  echo " "
  echo "Use: ./gitclone.sh <remote_branch_name>"
  echo "Example of use:"
  echo "./gitclone.sh MSNM_integration"
  echo " "
  exit 1
fi



#maquinas=(atacante borderRouter routerR1 routerR2 routerR3 m1.2 m2.2 m3.2 dmz wwwserver)
maquinas=(wwwserver)
DIR='git'
project_DIR='git/VERITASExperimentalScripts'
branch=$1

# removing the current project
rm -rf $project_DIR

for m in ${maquinas[*]}
do
	printf "[+] Connecting to: %s\n" $m
	eval $(printf "ssh nesg@%s \"cd %s; git clone --recursive git@metis.ugr.es:gmacia/VERITASExperimentalScripts -b %s\"\n" $m $DIR $branch)
done
