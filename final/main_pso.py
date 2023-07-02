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
from performance import calculate_efficiency_index
from PSO import PSO
import numpy as np
import time
import datetime
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
    average = 0
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
            average = sum(list_cycle)/len(list_cycle)
            if step % 180 == 0:
                print("{} Average_waiting_time : {:.2f}".format(step, average))

        step += 1

    print("Average_waiting_time: {:.2f}".format(average))
    traci.close()

    return average

def main():
    options = False
    run_step = 0
    result = []
    best_score = 99999999999

    # True : gui 실행없이 값만 출력, False : gui 실행
    if options == False:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # 초기 신호 설정값
    current_phases0 = [31.00, 3.00, 17.00, 3.00, 27.00, 3.00, 38.00, 3.00, 52.00, 3.00]
    current_phases1 = [33.00, 3.00, 17.00, 3.00, 22.00, 3.00, 32.00, 3.00, 61.00, 3.00]
    current_phases2 = [25.00, 3.00, 47.00, 3.00, 18.00, 3.00, 51.00, 3.00, 24.00, 3.00]

    # traci를 사용하여 sumo와 python을 연결
    while run_step < 10:
        print('{}번째 시뮬레이션'.format(run_step+1))
        generate_routefile() # 교통량 생성
        traci.start([sumoBinary, "-c", "tt.sumocfg", "--tripinfo-output", "tripinfo.xml", "--quit-on-end","--start", "--no-warnings"])
        
        # sumo에서 신호 세팅해주는 부분
        current_phases0, current_phases1, current_phases2 = modify_phase(current_phases0, current_phases1, current_phases2)

        # sumo 시뮬레이션 run 하는 부분 및 성능 추출하는 부분
        average = run()
        
        # current_phases0[0] -= 1
        # current_phases0[6] += 1
        # current_phases1[0] -= 1
        # current_phases1[6] += 1
        # current_phases2[0] -= 1
        # current_phases2[6] += 1

        result.append(average)
        run_step += 1

    result_average = sum(result) / len(result)
    print('result : ', result)
    print('{}번 시뮬레이션 : 평균 {:.2f}'.format(run_step, result_average))

    df = pd.DataFrame(result)
    df.to_csv('{}번 시뮬레이션 결과.csv'.format(run_step))

options = False
if options == False:
    sumoBinary = checkBinary('sumo')
else:
    sumoBinary = checkBinary('sumo-gui')

result = []
def objective_function(x):
    generate_routefile() # 교통량 생성
    
    x1 = np.array(x[:10])
    x2 = np.array(x[10:20])
    x3 = np.array(x[20:30])
    traci.start([sumoBinary, "-c", "tt.sumocfg", "--tripinfo-output", "tripinfo.xml", "--quit-on-end","--start", "--no-warnings"])
    modify_phase(x1, x2, x3)
    # if sum(x1) != 150:
    #     return sys.maxsize
    # elif sum(x2) != 150:
    #     return sys.maxsize
    # elif sum(x3) != 150:
    #     return sys.maxsize
    z = run()

    result.append([x, z])
    if len(result) % 300 ==0:
        pd.DataFrame(result).to_csv('result{}.csv'.format(len(result)), header=False, index=False)
    return z


min_dur = [10, 3, 10, 3, 10, 3, 10, 3, 10, 3,10, 3, 10, 3, 10, 3, 10, 3, 10, 3,10, 3, 10, 3, 10, 3, 10, 3, 10, 3]
max_dur = [30, 3, 30, 3, 30, 3, 30, 3, 30, 3,30, 3, 30, 3, 30, 3, 30, 3, 30, 3,30, 3, 30, 3, 30, 3, 30, 3, 30, 3]


if __name__ == "__main__":
    # main()
    start = time.time()
    bounds = []
    for i in range(len(min_dur)):
        bounds.append((min_dur[i], max_dur[i]))
    num_particles = 20
    maxiter = 2100
    pso = PSO(objective_function, bounds, num_particles, maxiter)
    pso.run_result()
    end = time.time()
    sec = end - start
    result_time = datetime.timedelta(seconds=(sec))
    print('총 걸린 시간 : ', result_time)
    # best_phase0, best_phase1, best_phase2, best_score = main()
    # print('첫번째 교차로 최적 신호주기 :', best_phase0)
    # print('두번째 교차로 최적 신호주기 :', best_phase1)
    # print('세번째 교차로 최적 신호주기 :', best_phase2)
    # print('최고 높은 점수는 :', best_score)