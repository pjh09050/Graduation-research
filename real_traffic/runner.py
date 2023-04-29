from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import optparse
import random
from sumolib import checkBinary  
import traci
from TrafficGenerator import TrafficGenerator

# we need to import python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")


def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options


# def run():
#     """execute the TraCI control loop"""
#     step = 0
#     # we start with phase 2 where EW has green
#     traci.trafficlight.setPhase("4", 0)
#     while traci.simulation.getMinExpectedNumber() > 0:
#         traci.simulationStep()
#         if traci.trafficlight.getPhase("4") == 2:
#             # we are not already switching
#             if traci.inductionloop.getLastStepVehicleNumber("4") > 0:
#                 # there is a vehicle from the north, switch
#                 traci.trafficlight.setPhase("4", 3)
#             else:
#                 # otherwise try to keep green for EW
#                 traci.trafficlight.setPhase("4", 2)
#         step += 1
#     traci.close()
#     sys.stdout.flush()

def run():
    step = 0
    max_step = 100
    while step < max_step+1:
        traci.simulationStep()
        step += 1
    traci.close()


if __name__ == "__main__":
    options = get_options()
    max_steps = 100

    # this script has been called from the command line. It will start sumo as a
    # server, then connect and run
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # 데이터가 뽑히는데 뭔지 모름
    # options = False
    # if options == False:
    #     sumoBinary = checkBinary('sumo')
    # else:
    #     sumoBinary = checkBinary('sumo-gui')

    # first, generate the route file for this simulation
    TrafficGenerator(max_steps)
    
    # this is the normal way of using traci. sumo is started as a subprocess and then the python script connects and runs
    traci.start([sumoBinary, "-c", "cross1.sumocfg","--tripinfo-output", "tripinfo.xml"])
    run()