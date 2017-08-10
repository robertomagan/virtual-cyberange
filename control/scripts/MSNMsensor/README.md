How to run an experiment step by step
-------------------------------------

1. Get sensor files from the gitlab repository: 
	* python setup_env config/scenario_#
2. Configure the *sensor.yaml* config file located in config dir in MSNMsensor for each involved sensor
3. Copy each modified *.yaml file to the corresponding sensor 
	* python setup_config config/scenario_#
4. Run the experiment. This script launch all sensors 
	* run.sh config/scenario_#
5. Copy the results obtained
	* copy_results.sh config/scenario_#

NOTE: all sensors behavior is logged in <sensor_name>/MSNMsensor/src/logs/msnm.log so you can monitor
how they are working.
