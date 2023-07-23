from __future__ import absolute_import
from __future__ import print_function

import os
import sys
from sumolib import checkBinary  
import traci
import pandas as pd
from TrafficGenerator import generate_routefile
from del_lane import del_lane

# $SUMO_HOME/tools directory에서 python module 가져와야 실행 가능
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")


def run():
    step = 0
    max_step = 3600
    del_lane()

    while step < max_step+1:
        traci.simulationStep()
        # 성능뽑을 떄 뒤에 1800 이후에 뽑아서 뒤에 30분만 평가하는게 현실적임
        step += 1
    traci.close()

def main():

    options = True
    if options == False:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    generate_routefile() 
    #traci.start([sumoBinary, "-c", "new.sumocfg", "--tripinfo-output", "tripinfo.xml", "--no-warnings"])
    traci.start([sumoBinary, "-c", "new.sumocfg", "--tripinfo-output", "tripinfo.xml", "--quit-on-end","--start", "--no-warnings"])
    run()

if __name__ == "__main__":
    main()
