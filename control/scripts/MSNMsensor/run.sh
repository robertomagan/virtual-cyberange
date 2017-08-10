#!/bin/bash

if [ "$#" -ne 1 ]; then
  echo " "
  echo "Use: ./run.sh <path_escenario>"
  echo "Example of use:"
  echo "<path_escenario>: config/scenario_1/"
  echo " "
  exit 1
fi

#input params
path_scenario=$1
online=$2

# setting up the environment
python setup_env.py $path_scenario

# setting up the sensors' configurations
python setup_config.py $path_scenario

# list of sensors
sensor_list=`cat $path_scenario/names.txt`
# current dir
curr_dir=`pwd`
# pids
pids=()

# launch sensors
for i in $sensor_list;
do
  cd $curr_dir/$i/MSNMsensor/src/
  python msnmsensor.py &>/dev/null &
  id=$!
  echo "Launching sensor $i with PID=$id"
  
  pids+=($id)

  cd $curr_dir
done

# launch offline simulation scripts
#if [ $online -eq 0 ]; then
  #echo "Launching offline scripts"
  #for i in $sensor_list;
  #do
  #  cd $curr_dir/$i/MSNMsensor/src/
  #  python static_simulation.py &>/dev/null &
  #  id=$!
  #  echo "Launching offline script for sensor $i with PID=$id"
    
  #  pids+=($id)

  #  cd $curr_dir
  #done
#fi

read -p "Push a key to stop all python processes gracefully ..."

for i in ${pids[@]};
do
  echo "Killing PID=$i"
  kill -n SIGINT $i
done

echo " "



