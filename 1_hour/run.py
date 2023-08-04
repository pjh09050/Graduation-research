from __future__ import absolute_import
from __future__ import print_function

import os
import sys
from sumolib import checkBinary  
import traci
from TrafficGenerator import generate_routefile
from modify_phase import modify_phase
from del_lane import del_lane
from performance import calculate_target_index

# $SUMO_HOME/tools directory에서 python module 가져와야 실행 가능
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")


def run():
    step = 0
    max_step = 3600
    cycle_list = []
    vehicle_travel_times = {}
    del_lane()
    
    while step < max_step+1:
        traci.simulationStep()
        step += 1

        if step > 1800:
            target_score = calculate_target_index()
            cycle_list.append(target_score)
            cycle_average = sum(cycle_list) / len(cycle_list)

            vehicle_ids = traci.vehicle.getIDList()
            for vehicle_id in vehicle_ids:
                if vehicle_id not in vehicle_travel_times:
                    vehicle_travel_times[vehicle_id] = 0
                vehicle_travel_times[vehicle_id] += 1
            average_travel_time_list = list(vehicle_travel_times.values())
            average_travel_time = sum(average_travel_time_list) / len(average_travel_time_list)

            if step % 180 == 0:
                print("{}초 평균 대기 시간 : {:.2f}".format(step, cycle_average))
                print("{}초 총 이탈 차량 수 : {}, 평균 이동 시간 : {}".format(step, len(vehicle_travel_times), average_travel_time))
        
    print("평균 대기 시간 : {:.3f}".format(cycle_average))
    print("평균 이동 시간 : {:.3f}".format(average_travel_time))
    traci.close()

def main():
    # 초기 신호 설정값
    current_phases0 = [31.00, 3.00, 17.00, 3.00, 27.00, 3.00, 38.00, 3.00, 52.00, 3.00] # (S-N:31),(S-W,N-E:17),(E-WS:27),(W-E:38),(W-NE:52)
    current_phases1 = [33.00, 3.00, 17.00, 3.00, 22.00, 3.00, 32.00, 3.00, 61.00, 3.00] # (S-N:33),(S-W,N-E:17),(E-WS:22),(W-E:32),(W-NE:61)
    current_phases2 = [66.00, 3.00, 18.00, 4.00, 3.00, 22.00, 3.00, 55.00, 3.00, 3.00] # (S-N:66),(S-N,S-W:18,4),(E-WS:22),(W-E:55) 마지막: 올적
    
    # PSO 중간
    current_phases0 = [27, 3, 22, 3, 26, 3, 42, 3, 48, 3] 
    current_phases1 = [31, 3, 19, 3, 19, 3, 35, 3, 61, 3] 
    current_phases2 = [55, 3, 20, 2, 3, 25, 3, 63, 3, 3]

    # PSO best
    # current_phases0 = [38, 3, 22, 3, 29, 3, 27, 3, 49, 3]
    # current_phases1 = [31, 3, 16, 3, 25, 3, 42, 3, 51, 3]
    # current_phases2 = [57, 3, 15, 5, 3, 62, 3, 26, 3, 3]

    options = True
    if options == False:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    traci.start([sumoBinary, "-c", "new.sumocfg", "--tripinfo-output", "tripinfo.xml", "--no-warnings"])
    # traci.start([sumoBinary, "-c", "new.sumocfg", "--tripinfo-output", "tripinfo.xml", "--quit-on-end","--start", "--no-warnings"])
    generate_routefile() 
    modify_phase(current_phases0, current_phases1, current_phases2)
    run()

if __name__ == "__main__":
    main()
