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
import pandas as pd

# $SUMO_HOME/tools directory에서 python module 가져와야 실행 가능
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

def run():
    step = 0
    max_step = 10800
    cycle_list = []
    left_right_list = []
    vehicle_travel_times = {}
    del_lane()
    
    while step < max_step+1:
        traci.simulationStep()
        step += 1

        if step > 3600:
            target_score, left_right = calculate_target_index()
            cycle_list.append(target_score)
            cycle_average = sum(cycle_list) / len(cycle_list)
            left_right_list.append(left_right)
            left_right_list_average = sum(left_right_list) / len(left_right_list)

            vehicle_ids = traci.vehicle.getIDList()
            for vehicle_id in vehicle_ids:
                if vehicle_id not in vehicle_travel_times:
                    vehicle_travel_times[vehicle_id] = 0
                vehicle_travel_times[vehicle_id] += 1
            average_travel_time_list = list(vehicle_travel_times.values())
            average_travel_time = sum(average_travel_time_list) / len(average_travel_time_list)

            if step % 180 == 0:
                print("{}초 평균 대기 시간 : {:.2f}".format(step, cycle_average))
                print("{}초 학교->정왕역 평균 대기 시간 : {:.2f}".format(step, left_right_list_average))
                print("{}초 학교->정왕역 최대 대기 시간 : {:.2f}".format(step, max(left_right_list)))
                print("{}초 총 이탈 차량 수 : {}, 평균 이동 시간 : {}".format(step, len(vehicle_travel_times), average_travel_time))
        
    print("평균 대기 시간 : {:.3f}".format(cycle_average))
    print("평균 이동 시간 : {:.3f}".format(average_travel_time))
    traci.close()
    return cycle_average, average_travel_time

def main():
    run_step = 0
    result = []
    travel_result = []
    
    # 초기 신호 설정값
    current_phases0 = [31, 3, 17, 3, 27, 3, 38, 3, 52, 3] # (S-N:31),(S-W,N-E:17),(E-WS:27),(W-E:38),(W-NE:52)
    current_phases1 = [33, 3, 17, 3, 22, 3, 32, 3, 61, 3] # (S-N:33),(S-W,N-E:17),(E-WS:22),(W-E:32),(W-NE:61)
    current_phases2 = [66, 3, 22, 3, 18, 4, 3, 55, 3, 3] # (S-N:66),(S-N,S-W:18,4),(E-WS:22),(W-E:55) 마지막: 올적

    # 경험 신호주기
    # current_phases0 = [26, 3, 17, 3, 27, 3, 43, 3, 52, 3]
    # current_phases1 = [26, 3, 17, 3, 22, 3, 39, 3, 61, 3]
    # current_phases2 = [60, 3, 22, 3, 18, 4, 3, 61, 3, 3]

    # 3시간 PSO
    # current_phases0 = [26, 3, 15, 3, 25, 3, 48, 3, 51, 3]
    # current_phases1 = [26, 3, 22, 3, 17, 3, 42, 3, 58, 3]
    # current_phases2 = [56, 3, 15, 3, 21, 8, 3, 65, 3, 3]
                        
    # 3시간 PSO_정규화_가상 데이터
    # current_phases0 = [27, 3, 16, 3, 23, 3, 53, 3, 46, 3]
    # current_phases1 = [41, 3, 15, 3, 14, 3, 40, 3, 55, 3]
    # current_phases2 = [56, 3, 19, 3, 19, 6, 3, 65, 3, 3]

    # 3시간 PSO_정규화_실제 데이터
    # current_phases0 = [32, 3, 8, 3, 27, 3, 42, 3, 56, 3]
    # current_phases1 = [27, 3, 19, 3, 28, 3, 33, 3, 58, 3]
    # current_phases2 = [55, 3, 17, 3, 21, 6, 3, 66, 3, 3]

    # 3시간 PSO_정규화_최종
    # current_phases0 = [26, 3, 23, 3, 23, 3, 46, 3, 47, 3]
    # current_phases1 = [37, 3, 10, 3, 24, 3, 37, 3, 57, 3] 
    # current_phases2 = [60, 3, 20, 3, 13, 2, 3, 70, 3, 3]

    options = True
    if options == False:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    while run_step < 10:
        print('{}번째 시뮬레이션'.format(run_step+1))
        generate_routefile() # 교통량 생성S

        # traci를 사용하여 sumo와 python을 연결
        # traci.start([sumoBinary, "-c", "new.sumocfg", "--tripinfo-output", "tripinfo.xml", "--quit-on-end","--start", "--no-warnings"])
        traci.start([sumoBinary, "-c", "new.sumocfg", "--tripinfo-output", "tripinfo.xml", "--quit-on-end", "--no-warnings"])
        # sumo에서 신호 세팅해주는 부분
        current_phases0, current_phases1, current_phases2 = modify_phase(current_phases0, current_phases1, current_phases2)

        # sumo 시뮬레이션  성능 추출하는 부분
        average, average_travel_time = run()

        result.append(average)
        travel_result.append(average_travel_time)

        run_step += 1

    result_average = sum(result) / len(result)
    travel_result_average = sum(travel_result) / len(travel_result)

    print("" "")
    print('Average_travel_time : ', result)
    print("Average_waiting_time : ", travel_result)
    print('{}번 시뮬레이션 : 평균 대기 시간 {:.2f}, 평균 이동 시간 {:.2f}'.format(run_step, result_average, travel_result_average))
    print("" "")
    df = pd.DataFrame([result, travel_result])
    df.to_csv('{}번 시뮬레이션 결과.csv'.format(run_step))

if __name__ == "__main__":
    main()
