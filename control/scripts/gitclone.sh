#!/bin/bash

# Este script realiza un borrado del proyecto y luego un git clone recursivo en el directorio ~/git/ para una rama en concreto
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
project_DIR='VERITASExperimentalScripts'
branch=$1

for m in ${maquinas[*]}
do
	printf "[+] Connecting to: %s\n" $m
	eval $(printf "ssh nesg@%s \"cd %s; rm -rf %s; git clone git@192.168.56.1:gmacia/VERITASExperimentalScripts -b %s; cd %s; git config --file=.gitmodules submodule.machines/MSNMsensor.url ssh://git@192.168.56.1/robertomagan/MSNMsensor.git; git submodule update --init --recursive\"\n" $m $DIR $project_DIR $branch $project_DIR)
done
