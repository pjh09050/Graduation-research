from __future__ import absolute_import
from __future__ import print_function

import os
import sys
from sumolib import checkBinary  
import traci
import numpy as np
from TrafficGenerator import generate_routefile
from modify_phase import modify_phase
from del_lane import del_lane
from performance import calculate_efficiency_index

# we need to import python modules from the $SUMO_HOME/tools directory
# $SUMO_HOME/tools directory에서 python module 가져와야 실행 가능
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

def run():
    step = 0
    max_step = 3600
    average_list = []
    list_cycle = []
    high_score = -99999999999
    # 불필요한 라인 지운 후 라인 확인
    lane_ids = del_lane()
    #print(len(lane_ids))
    #print(lane_ids)
    
    while step < max_step+1:
        traci.simulationStep()

        # 교차로 효율성 지수 측정할 if문 (기준을 어떻게 잡지?)(lane_ids에서 차선별로 구분지어서 좌우는 좀더 가중치 주기?)
        if step > 180:
            efficiency_index = calculate_efficiency_index()
            list_cycle.append(efficiency_index)
            cycle_average = sum(list_cycle)/len(list_cycle)
            if step % 180 == 0:
                #print("{} step Efficiency Index: {:.2f}".format(step ,cycle_average))
                print("{} step Average_waiting_time: {:.2f}".format(step, cycle_average))
                list_cycle = []
            average_list.append(cycle_average)
        step += 1

    average = sum(average_list)/len(average_list)
    if high_score <= average:
        high_score = average
    #print("Efficiency average: {:.2f}".format(average))
    print("Average_waiting_time: {:.2f}".format(average))
    traci.close()
    #return np.round(average,2)
    return average, high_score

def main():
    options = False
    run_step = 0
    result = []
    best_score = 99999999999

    # this script has been called from the command line. It will start sumo as a server, then connect and run
    # True : gui 실행없이 값만 출력, False : gui 실행
    if options == False:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # first, generate the route file for this simulation
    # 첫번째 교통량 생성
    generate_routefile()
    
    # 초기 신호 설정값
    current_phases0 = [31.00, 3.00, 17.00, 3.00, 27.00, 3.00, 38.00, 3.00, 52.00, 3.00]
    current_phases1 = [33.00, 3.00, 17.00, 3.00, 22.00, 3.00, 32.00, 3.00, 61.00, 3.00]
    current_phases2 = [25.00, 3.00, 47.00, 3.00, 18.00, 3.00, 51.00, 3.00, 24.00, 3.00]

    # this is the normal way of using traci. sumo is started as a subprocess and then the python script connects and runs
    # traci를 사용하여 sumo와 python을 연결
    while run_step < 10:
        traci.start([sumoBinary, "-c", "tt.sumocfg", "--tripinfo-output", "tripinfo.xml", "--quit-on-end","--start"])
        modify_phases0, modify_phases1, modify_phases2 = modify_phase(current_phases0, current_phases1, current_phases2)
        print('{}번째 시뮬레이션'.format(run_step+1))
        average, high_score = run()
        
        if best_score >= high_score:
            best_score = high_score
            best_phase0 = modify_phases0[:]
            best_phase1 = modify_phases1[:]
            best_phase2 = modify_phases2[:]
        
        # modify_phases0[0] -+ 1
        # modify_phases0[6] += 1
        # modify_phases1[0] -+ 1
        # modify_phases1[6] += 1
        # modify_phases2[0] -+ 1
        # modify_phases2[6] += 1
        current_phases0 = modify_phases0[:]
        current_phases1 = modify_phases1[:]
        current_phases2 = modify_phases2[:]
        
        result.append(average)
        generate_routefile()
        run_step += 1

    result_average = sum(result) / len(result)
    print('result : ', result)
    print('{}번 시뮬레이션 : 평균 {:.2f}'.format(run_step, result_average))
    print(best_phase0, best_phase1, best_phase2)
    return best_phase0, best_phase1, best_phase2, best_score

if __name__ == "__main__":
    best_phase0, best_phase1, best_phase2, best_score = main()
    print('첫번째 교차로 최적 신호주기 :', best_phase0)
    print('두번째 교차로 최적 신호주기 :', best_phase1)
    print('세번째 교차로 최적 신호주기 :', best_phase2)
    print('최고 높은 점수는 :', best_score)