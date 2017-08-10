import os
import sys
import shutil
from subprocess import call

# Check the number of scripts params

nparams = len(sys.argv)

if nparams == 1:
  print "Use: setup_config.py <path_scenario>"
  exit(1)

# path of the scenario
scenario = sys.argv[1]


# list of sensors
sensors = []
with open(scenario + "/names.txt","r") as f:
  line = f.readline().rstrip('\n')
  for i in line.split(' '):
    sensors.append(i)

# current dir
curr_dir = os.getcwd()

# sensor configurations dir
config_dir = curr_dir + os.sep + scenario

# setup sensors configuration previously 
for i in sensors:
  try:
    print "Copy config file of sensor %s ..." %(i)
    call('scp ' + config_dir + os.sep + i + '.yaml nesg@' + i + ':~/git/VERITASExperimentalScripts/machines/MSNMsensor/src/config/')
  except Exception:
    print "Error copying config file of sensor %s: %s" %(i,sys.exc_info()[1])

print " "



