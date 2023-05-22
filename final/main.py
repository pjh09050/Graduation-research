from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import optparse
import random
from sumolib import checkBinary  
import traci
from TrafficGenerator import generate_routefile

# we need to import python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

def calculate_efficiency_index():
    # 대기 시간 추출
    lane_ids = traci.lane.getIDList()
    waiting_times = [traci.lane.getWaitingTime(lane_id) for lane_id in lane_ids]
    average_waiting_time = sum(waiting_times) / len(waiting_times)

    # 대기 차량 비율 추출
    waiting_vehicle_count = sum([traci.lane.getLastStepHaltingNumber(lane_id) for lane_id in lane_ids])
    total_vehicle_count = sum([traci.lane.getLastStepVehicleNumber(lane_id) for lane_id in lane_ids])
    waiting_vehicle_ratio = waiting_vehicle_count / total_vehicle_count

    # 통과 차량 비율 추출
    passing_vehicle_count = total_vehicle_count - waiting_vehicle_count
    passing_vehicle_ratio = passing_vehicle_count / total_vehicle_count

    # 효율성 지수 계산
    scaled_waiting_time = average_waiting_time / max(waiting_times)
    efficiency_index = passing_vehicle_ratio / (scaled_waiting_time + waiting_vehicle_ratio)

    return efficiency_index

def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options

def run():
    step = 0
    max_step = 3600
    while step < max_step+1:
        traci.simulationStep()
        if step > 100 and step % 10 == 0:
            efficiency_index = calculate_efficiency_index()
            print("Efficiency Index: {:.2f}".format(efficiency_index))
        #min_expected_number = traci.simulation.getMinExpectedNumber()
        #print(f"Step {step}: Min Expected Number: {min_expected_number}")
        step += 1
    traci.close()


if __name__ == "__main__":
    options = get_options()

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
    generate_routefile()

    # this is the normal way of using traci. sumo is started as a subprocess and then the python script connects and runs
    traci.start([sumoBinary, "-c", "tt.sumocfg","--tripinfo-output", "tripinfo.xml"])

    run()