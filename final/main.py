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
        set_phase()
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
    # 신호등 ID 목록 가져오기
    traffic_light_ids = traci.trafficlight.getIDList()
    print("Traffic light IDs:", traffic_light_ids)

    # 새로운 주기 상태 설정
    new_phases = {traffic_light_ids[0]: {0: 31.00, 1: 3.00, 2: 17.00, 3: 3.00, 4: 27.00, 5: 3.00, 6: 38.00, 7: 3.00, 8: 52.00, 9: 2.00}}  # 각 신호의 주기 설정

    # 주기 변경
    # 주기 변경
    for traffic_light_id, phases in new_phases.items():
        for phase_id, duration in phases.items():
            print(traffic_light_id, phase_id, duration)
            traci.trafficlight.setPhaseDuration(traffic_light_id, phase_id, duration)

    # 변경된 주기 확인
    for traffic_light_id in traffic_light_ids:
        phases = traci.trafficlight.getCompleteRedYellowGreenDefinition(traffic_light_id)
        print("Current phases of", traffic_light_id, ":", phases)


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