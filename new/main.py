from __future__ import absolute_import
from __future__ import print_function

import os
import sys
from sumolib import checkBinary  
import traci
import pandas as pd
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
    list_cycle = []
    vehicle_travel_times = {}
    del_lane()    # 불필요한 라인 지우기

    while step < max_step+1:
        traci.simulationStep()

        if step > 600:
            target_score = calculate_target_index()
            list_cycle.append(target_score)
            average = sum(list_cycle)/len(list_cycle)

            vehicle_ids = traci.vehicle.getIDList()
            for vehicle_id in vehicle_ids:
                if vehicle_id not in vehicle_travel_times:
                    vehicle_travel_times[vehicle_id] = 0
                vehicle_travel_times[vehicle_id] += 1
            average_travel_time_list = list(vehicle_travel_times.values())
            average_travel_time = sum(average_travel_time_list) / len(average_travel_time_list)

            if step % 180 == 0:
                print("{}초 평균 대기 시간 : {:.2f}".format(step, average))
                print("{}초 총 이탈 차량 수 : {}, 평균 이동 시간 : {}".format(step, len(vehicle_travel_times), average_travel_time))

        step += 1
    print("평균 대기 시간 : {:.3f}".format(average))
    print("평균 이동 시간 : {:.3f}".format(average_travel_time))
    traci.close()
    return average, average_travel_time

def main():
    options = True
    run_step = 0
    result = []
    travel_result = []

    # True : gui 실행없이 값만 출력, False : gui 실행
    if options == False:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # 초기 신호 설정값
    # current_phases0 = [31.00, 3.00, 17.00, 3.00, 27.00, 3.00, 38.00, 3.00, 52.00, 3.00]
    # current_phases1 = [33.00, 3.00, 17.00, 3.00, 22.00, 3.00, 32.00, 3.00, 61.00, 3.00]
    # current_phases2 = [25.00, 3.00, 47.00, 3.00, 18.00, 3.00, 51.00, 3.00, 24.00, 3.00]
    
    # 13번신호 설정값    
    current_phases0 = [26.00, 3.00, 17.00, 3.00, 27.00, 3.00, 43.00, 3.00, 52.00, 3.00]
    current_phases1 = [26.00, 3.00, 17.00, 3.00, 22.00, 3.00, 39.00, 3.00, 61.00, 3.00]
    current_phases2 = [22.00, 3.00, 42.00, 3.00, 21.00, 3.00, 56.00, 3.00, 24.00, 3.00]

    while run_step < 10:
        print('{}번째 시뮬레이션'.format(run_step+1))
        generate_routefile() # 교통량 생성

        # traci를 사용하여 sumo와 python을 연결
        # traci.start([sumoBinary, "-c", "tt.sumocfg", "--tripinfo-output", "tripinfo.xml", "--quit-on-end", "--start", "--no-warnings"])
        traci.start([sumoBinary, "-c", "tt.sumocfg", "--tripinfo-output", "tripinfo.xml", "--quit-on-end", "--no-warnings"])
        
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
    print("Average_waiting_time : ", travel_result_average)
    print('{}번 시뮬레이션 : 평균 대기 시간 {:.2f}, 평균 이동 시간 {:.2f}'.format(run_step, result_average, travel_result_average))
    print("" "")
    #df = pd.DataFrame(result)
    #df.to_csv('{}번 시뮬레이션 결과.csv'.format(run_step))

if __name__ == "__main__":
    main()