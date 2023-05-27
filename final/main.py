from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import optparse
from sumolib import checkBinary  
import traci
from TrafficGenerator import generate_routefile
from modify_phase import modify_phase
from del_lane import del_lane
from performance import calculate_efficiency_index

# we need to import python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

# def get_options():
#     optParser = optparse.OptionParser()
#     optParser.add_option("--nogui", action="store_true", default=False, help="run the commandline version of sumo")
#     options, args = optParser.parse_args()
#     return options

def run():
    step = 0
    max_step = 3600
    average_list = []
    modify_phase()
    lane_ids = del_lane()
    print(len(lane_ids))
    print(lane_ids)
    
    while step < max_step+1:
        traci.simulationStep()

        # 교차로 효율성 지수 측정할 if문 (기준을 어떻게 잡지?)(lane_ids에서 차선별로 구분지어서 좌우는 좀더 가중치 주기?)
        if step > 100 and step % 10 == 0:
            efficiency_index = calculate_efficiency_index()
            average_list.append(efficiency_index)
            print("Efficiency Index: {:.2f}".format(efficiency_index))
        step += 1

    average = sum(average_list)/len(average_list)
    print("Efficiency average: {:.2f}".format(average))
    traci.close()
    return average

def main():
    #options = get_options()
    options = False
    run_step = 0
    result = []

    # this script has been called from the command line. It will start sumo as a server, then connect and run
    #if options.nogui:
    if options == True:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # first, generate the route file for this simulation
    generate_routefile()

    # this is the normal way of using traci. sumo is started as a subprocess and then the python script connects and runs
    while run_step < 2:
        traci.start([sumoBinary, "-c", "tt.sumocfg", "--tripinfo-output", "tripinfo.xml", "--quit-on-end", "--start"])
        average = run()
        result.append(average)
        generate_routefile()
        run_step += 1

    result_average = sum(result) / len(result)
    print('result : {:.2f}',result)
    print('{}번 시뮬레이션 : 평균 {:.2f}'.format(run_step, result_average))

if __name__ == "__main__":
    main()