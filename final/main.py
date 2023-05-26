from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import optparse
import subprocess
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
    average = []
    
    while step < max_step+1:
        traci.simulationStep()
        set_phase()
        lane_ids = list(traci.lane.getIDList())
        # todo : 필요없는 lane 지우기
        del_list = ['00to01_3', '00to3_3', '00to2_3', '00to000_3', '000to00_3', '000to0000_4', '000to0000_0', '0000to000_3', '0000to11_4', '0000to10_4', '0000to04_4', '0000to04_0', '001to003_0', '004to002_0'
                    , '005to007_0', '008to006_0']
        for i in del_list:
            if i in lane_ids:
                lane_ids.remove(i)
        # todo 확인용 if문
        if step == 1:
            print(len(lane_ids))
            print(lane_ids)
        # 교차로 효율성 지수 측정할 if문 (기준을 어떻게 잡지?)
        if step > 100 and step % 10 == 0:
            efficiency_index = calculate_efficiency_index()
            average.append(efficiency_index)
            print("Efficiency Index: {:.2f}".format(efficiency_index))
        step += 1
        #change_phase()
        
    print("Efficiency average: {:.2f}".format(sum(average)/len(average)))
    traci.close()

def change_phase():
    # 신호등 ID 목록 가져오기
    traffic_light_ids = traci.trafficlight.getIDList()
    print("Traffic light IDs:", traffic_light_ids) # 리스트 길이 3 [00, 000, 0000]

    # 신호등의 현재 주기 정보 가져오기
    first_phase = traci.trafficlight.getPhase(traffic_light_ids[0])
    second_phase = traci.trafficlight.getPhase(traffic_light_ids[1])
    third_phase = traci.trafficlight.getPhase(traffic_light_ids[2])
    print("first phase : {}, second phase : {}, third phase : {}".format(first_phase, second_phase, third_phase))

    # 주기 변경
    first_phase_time = traci.trafficlight.getPhaseDuration(traffic_light_ids[0])
    second_phase_time = traci.trafficlight.getPhaseDuration(traffic_light_ids[1])
    third_phase_time = traci.trafficlight.getPhaseDuration(traffic_light_ids[2])
    print("first phase time : {}, second phase time : {}, third phase time : {}".format(first_phase_time, second_phase_time, third_phase_time))
    # new_phase = (current_phase + 1) % traci.trafficlight.getPhaseDuration(traffic_light_id)
    # traci.trafficlight.setPhase(traffic_light_id, new_phase)
    # print("New phase:", new_phase)

def set_phase():
    # 신호등 ID 가져오기
    traffic_light_id0 = traci.trafficlight.getIDList()[0]
    traffic_light_id1 = traci.trafficlight.getIDList()[0]
    traffic_light_id2 = traci.trafficlight.getIDList()[0]
    
    #print("Traffic light ID:", traffic_light_id)
    
    # 현재 phase
    current_phases0 = [31.00, 3.00, 17.00, 3.00, 27.00, 3.00, 38.00, 3.00, 52.00, 3.00]
    current_phases1 = [33.00, 3.00, 17.00, 3.00, 22.00, 3.00, 32.00, 3.00, 61.00, 3.00]
    current_phases2 = [25.00, 3.00, 47.00, 3.00, 18.00, 3.00, 51.00, 3.00, 24.00, 3.00]
    
    # 새로운 phase
    new_phases0 = [31.00, 3.00, 17.00, 3.00, 27.00, 3.00, 38.00, 3.00, 52.00, 3.00]
    new_phases1 = [21.00, 3.00, 12.00, 3.00, 25.00, 3.00, 55.00, 3.00, 52.00, 3.00]
    new_phases2 = [21.00, 3.00, 12.00, 3.00, 25.00, 3.00, 55.00, 3.00, 52.00, 3.00]

    ### '00' 신호등 의 모든 phase 정보 가져오기 ###
    complete_definition0 = traci.trafficlight.getCompleteRedYellowGreenDefinition(traffic_light_id0)
    for i, phase in enumerate(complete_definition0[0].phases):
        phase.duration = new_phases0[i]  # new_phases의 duration 값을 할당합니다.
        phase.minDur = new_phases0[i]
        phase.maxDur = new_phases0[i]
    # 수정된 신호등 phase 정보를 시뮬레이터에 적용
    traci.trafficlight.setCompleteRedYellowGreenDefinition(traffic_light_id0, complete_definition0[0])
    # 수정된 신호등 phase 정보 확인
    modify_phases0 = traci.trafficlight.getCompleteRedYellowGreenDefinition(traffic_light_id0)
    #print(modify_phases0[0].phases)

    ### '000' 신호등 의 모든 phase 정보 가져오기 ###
    complete_definition1 = traci.trafficlight.getCompleteRedYellowGreenDefinition(traffic_light_id1)
    for i, phase in enumerate(complete_definition1[0].phases):
        phase.duration = new_phases1[i]  # new_phases의 duration 값을 할당합니다.
        phase.minDur = new_phases1[i]
        phase.maxDur = new_phases1[i]
    # 수정된 신호등 phase 정보를 시뮬레이터에 적용
    traci.trafficlight.setCompleteRedYellowGreenDefinition(traffic_light_id1, complete_definition1[0])
    # 수정된 신호등 phase 정보 확인
    modify_phases1 = traci.trafficlight.getCompleteRedYellowGreenDefinition(traffic_light_id1)
    #print(modify_phases1[0].phases)

    ### '0000' 신호등 의 모든 phase 정보 가져오기 ###
    complete_definition2 = traci.trafficlight.getCompleteRedYellowGreenDefinition(traffic_light_id2)
    for i, phase in enumerate(complete_definition2[0].phases):
        phase.duration = new_phases2[i]  # new_phases의 duration 값을 할당합니다.
        phase.minDur = new_phases2[i]
        phase.maxDur = new_phases2[i]
    # 수정된 신호등 phase 정보를 시뮬레이터에 적용
    traci.trafficlight.setCompleteRedYellowGreenDefinition(traffic_light_id2, complete_definition2[0])
    # 수정된 신호등 phase 정보 확인
    modify_phases2 = traci.trafficlight.getCompleteRedYellowGreenDefinition(traffic_light_id2)
    #print(modify_phases2[0].phases)


if __name__ == "__main__":
    options = get_options()

    # this script has been called from the command line. It will start sumo as a
    # server, then connect and run
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # first, generate the route file for this simulation
    generate_routefile()

    # this is the normal way of using traci. sumo is started as a subprocess and then the python script connects and runs
    traci.start([sumoBinary, "-c", "tt.sumocfg","--tripinfo-output", "tripinfo.xml"])
    
    run()

# def main():
#     options = get_options()

#     sumo_binary = "sumo" if options.nogui else "sumo-gui"

#     while True:
#         # 차량 생성
#         generate_routefile()

#         # this is the normal way of using traci. sumo is started as a subprocess and then the python script connects and runs
#         traci.start([sumo_binary, "-c", "tt.sumocfg","--tripinfo-output", "tripinfo.xml"])

#         run()

#         # 사용자 입력 받기Q
#         user_input = input("Press 'R' to restart, or 'Q' to quit: ")

#         if user_input.lower() == 'r':
#             continue  # 다시 실행
#         elif user_input.lower() == 'q':
#             break  # 종료

# if __name__ == "__main__":
#     main()