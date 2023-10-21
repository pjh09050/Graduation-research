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
import matplotlib.pyplot as plt
plt.rc('font', family='Malgun Gothic')
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
    all_direction_list = []
    right_left_waiting_time = []
    left_right_waiting_time = []
    up_down_waiting_time = []
    down_up_waiting_time = []
    average_waiting_time_list = []
    vehicle_travel_times = {}

    del_lane()

    while step < max_step+1:
        traci.simulationStep()
        step += 1

        # if step > 100:
        #     vehicle_ids = traci.vehicle.getIDList()
        #     for vehicle_id in vehicle_ids:
        #         if vehicle_id not in vehicle_travel_times:
        #             vehicle_travel_times[vehicle_id] = 0
        #         vehicle_travel_times[vehicle_id] += 1
        #     average_travel_time_list = list(vehicle_travel_times.values())
        #     travel_time_average = sum(average_travel_time_list) / len(average_travel_time_list)

        if step > 3600:
            # 평균 뽑아오기
            all_direction, right_left, left_right, up_down, down_up = calculate_target_index()
            # 모든 방향 평균 
            all_direction_list.append(all_direction)
            all_direction_average = sum(all_direction_list) / len(all_direction_list)
            # 모든 방향 평균 모아놓기
            average_waiting_time_list.append(all_direction_average)
            # 학교 <- 정왕역
            right_left_waiting_time.append(right_left)
            right_left_list_average = sum(right_left_waiting_time) / len(right_left_waiting_time)
            # 학교 -> 정왕역
            left_right_waiting_time.append(left_right)
            left_right_list_average = sum(left_right_waiting_time) / len(left_right_waiting_time)
            # 48 -> 49
            up_down_waiting_time.append(up_down)
            up_down_list_average = sum(up_down_waiting_time) / len(up_down_waiting_time)
            # 48 <- 49
            down_up_waiting_time.append(down_up)
            down_up_list_average = sum(down_up_waiting_time) / len(down_up_waiting_time)
            if step % 180 == 0:
                print("{}초 평균 대기 시간 : {:.2f}".format(step, all_direction_average))
                print("{}초 학교 <- 정왕역 평균 대기 시간 : {:.2f}".format(step, right_left_list_average))
                # print("{}초 학교<-정왕역 최대 대기 시간 : {:.2f}".format(step, max(right_left_waiting_time)))
                print("{}초 학교 -> 정왕역 평균 대기 시간 : {:.2f}".format(step, left_right_list_average))
                # print("{}초 학교->정왕역 최대 대기 시간 : {:.2f}".format(step, max(left_right_waiting_time)))
                print("{}초 48 -> 49 평균 대기 시간 : {:.2f}".format(step, up_down_list_average))
                print("{}초 48 <- 49 평균 대기 시간 : {:.2f}".format(step, down_up_list_average))
                # print("{}초 총 이탈 차량 수 : {}, 평균 이동 시간 : {}".format(step, len(vehicle_travel_times), travel_time_average))

    print("평균 대기 시간 : {:.3f}".format(all_direction_average))
    traci.close()
    # plt.plot(range(3780, step), average_waiting_time_list[180:])
    # plt.xlabel('Time Step (단위:분)', fontsize=14)
    # plt.ylabel('Average Waiting Time (단위:분)', fontsize=14)
    # plt.title('출근 시간대 Simulation result', fontsize=16)
    # plt.show()
    return average_waiting_time_list, all_direction_average, left_right_list_average, max(left_right_waiting_time), right_left_list_average, max(right_left_waiting_time), up_down_list_average, down_up_list_average

def main():
    run_step = 0
    # 기존 신호 설정값
    current_phases0 = [45, 3, 17, 3, 27, 3, 58, 3, 18, 3]
    current_phases1 = [41, 3, 17, 3, 27, 3, 52, 3, 28, 3] 
    current_phases2 = [66, 3, 22, 3, 18, 4, 3, 55, 3, 3] 

    # 3시간 PSO
    current_phases3 = [38, 3, 20, 3, 24, 3, 65, 3, 18, 3]
    current_phases4 = [34, 3, 13, 3, 25, 3, 60, 3, 33, 3]
    current_phases5 = [54, 3, 20, 3, 22, 6, 3, 63, 3, 3]

    options = False
    if options == False:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')
#####################################################################################################################################################################################

    waiting_result = []
    left_right_result = []
    left_right_max_waiting_result = []
    right_left_result = []
    right_left_max_waiting_result = []
    up_down_result = []
    down_up_result = []
    # travel_result = []

    while run_step < 10:
        print('{}번째 시뮬레이션'.format(run_step+1))
        generate_routefile() # 교통량 생성

        # traci를 사용하여 sumo와 python을 연결
        traci.start([sumoBinary, "-c", "new1.sumocfg", "--tripinfo-output", "tripinfo.xml", "--quit-on-end","--start", "--no-warnings"])
        # traci.start([sumoBinary, "-c", "new1.sumocfg", "--tripinfo-output", "tripinfo.xml", "--quit-on-end", "--no-warnings"])
        # sumo에서 신호 세팅해주는 부분
        current_phases0, current_phases1, current_phases2 = modify_phase(current_phases0, current_phases1, current_phases2)

        # sumo 시뮬레이션  성능 추출하는 부분
        average_waiting_time_list, all_direction_average, left_right_list_average, max_waiting_time, right_left_list_average, left_right_waiting_time, up_down_list_average, down_up_list_average = run()

        waiting_result.append(all_direction_average)
        left_right_result.append(left_right_list_average)
        # left_right_max_waiting_result.append(max_waiting_time)
        right_left_result.append(right_left_list_average)
        # right_left_max_waiting_result.append(left_right_waiting_time)
        up_down_result.append(up_down_list_average)
        down_up_result.append(down_up_list_average)
        # travel_result.append(average_travel_time)

        run_step += 1
#####################################################################################################################################################################################

    run_step = 0
    waiting_result1 = []
    left_right_result1 = []
    right_left_result1 = []
    up_down_result1 = []
    down_up_result1 = []
    # travel_result1 = []

    while run_step < 10:
        print('{}번째 시뮬레이션'.format(run_step+1))
        generate_routefile() # 교통량 생성

        # traci를 사용하여 sumo와 python을 연결
        traci.start([sumoBinary, "-c", "new1.sumocfg", "--tripinfo-output", "tripinfo.xml", "--quit-on-end","--start", "--no-warnings"])
        # traci.start([sumoBinary, "-c", "new1.sumocfg", "--tripinfo-output", "tripinfo.xml", "--quit-on-end", "--no-warnings"])
        # sumo에서 신호 세팅해주는 부분
        current_phases3, current_phases4, current_phases5 = modify_phase(current_phases3, current_phases4, current_phases5)

        # sumo 시뮬레이션  성능 추출하는 부분
        average_waiting_time_list1, all_direction_average1, left_right_list_average1, max_waiting_time1, right_left_list_average1, left_right_waiting_time1, up_down_list_average1, down_up_list_average1 = run()

        waiting_result1.append(all_direction_average1)
        left_right_result1.append(left_right_list_average1)
        # left_right_max_waiting_result1.append(max_waiting_time1)
        right_left_result1.append(right_left_list_average1)
        # right_left_max_waiting_result1.append(left_right_waiting_time1)
        up_down_result1.append(up_down_list_average1)
        down_up_result1.append(down_up_list_average1)
        # travel_result1.append(average_travel_time1)

        run_step += 1
#####################################################################################################################################################################################

    # print('Average_waiting_time : ', waiting_result)
    # print('{}번 시뮬레이션 : 평균 대기 시간 {:.2f}'.format(run_step, waiting_result_average))
    # print("" "")

    print('waiting_result = ', waiting_result)
    print('waiting_result1 = ', waiting_result1)

    print('left_right_result = ', left_right_result)
    print('left_right_result1 = ', left_right_result1)

    print('right_left_result = ', right_left_result)
    print('right_left_result1 = ', right_left_result1)

    print('up_down result = ', up_down_result)
    print('up_down result1 = ', up_down_result1)

    print('down_up result = ', down_up_result)
    print('down_up result1 = ', down_up_result1)

#####################################################################################################################################################################################
    waiting_data = [waiting_result, waiting_result1]
    left_right_data = [left_right_result, left_right_result1]
    right_left_data = [right_left_result, right_left_result1]
    up_down_data = [up_down_result, up_down_result1]
    down_up_data = [down_up_result, down_up_result1]

    data_categories = [waiting_data, left_right_data, right_left_data, up_down_data, down_up_data]
    category_names = ['모든 방향', '학교 -> 정왕역', '정왕역 -> 학교', '월곶 -> 안산', '안산 -> 월곶']

    fig, axes = plt.subplots(2, 3, figsize=(20, 15), sharey=False, gridspec_kw={'wspace': 0.3, 'hspace': 0.3})
    for i, ax in enumerate(axes.flat[:-1]):
        if i < len(data_categories):
            boxplot = ax.boxplot(data_categories[i])
            for box in boxplot['boxes']:
                box.set(linewidth=1)
            ax.set_title(category_names[i], fontsize=20)
            ax.set_xticklabels(['기존 신호', '제안 신호'], fontsize=16)
            ax.set_ylabel('평균 대기시간 (초)', fontsize=16)
            ax.tick_params(axis='both', labelsize=16)

    fig.delaxes(axes[1, 2])
    plt.subplots_adjust(top=0.8)
    plt.show()
#####################################################################################################################################################################################
    waiting_data = [waiting_result, waiting_result1]
    left_right_data = [left_right_result, left_right_result1]
    right_left_data = [right_left_result, right_left_result1]
    up_down_data = [up_down_result, up_down_result1]
    down_up_data = [down_up_result, down_up_result1]

    data_categories = [waiting_data, left_right_data, right_left_data, up_down_data, down_up_data]
    category_names = ['모든 방향', '학교 -> 정왕역', '정왕역 -> 학교', '월곶 -> 안산', '안산 -> 월곶']

    fig, axes = plt.subplots(1, 5, figsize=(30, 8), sharey=False, gridspec_kw={'wspace': 0.3})
    for i, ax in enumerate(axes):
        boxplot = ax.boxplot(data_categories[i])
        for box in boxplot['boxes']:
            box.set(linewidth=1)
        ax.set_title(category_names[i], fontsize=20)
        ax.set_xticklabels(['기존 신호', '제안 신호'], fontsize=16)
        ax.set_ylabel('평균 대기시간 (초)', fontsize=16)
        ax.tick_params(axis='both', labelsize=16)

    plt.subplots_adjust(top=0.8)
    plt.show()
#####################################################################################################################################################################################

    # print('right_left_max_waiting_result = ', right_left_max_waiting_result)
    # print('right_left_max_waiting_result1 = ', right_left_max_waiting_result5)
    
    # print('travel_result = ', travel_result)
    # print('travel_result1 = ', travel_result5)
    
    # plt.figure(figsize=(12,8))
    # plt.boxplot([waiting_result, waiting_result1, waiting_result2, waiting_result3])
    # plt.xticks([1,2,3,4], labels=['현재 신호', 'PSO 1 신호', 'PSO 2 신호', 'PSO 3 신호'], fontsize=20)
    # plt.yticks(fontsize=20)
    # plt.xlabel('평균 대기시간 (초)', fontsize=20)
    # plt.ylabel('평균 대기시간 (초)', fontsize=20)
    # plt.title('퇴근 시간대 Simulation results of 10 iterations', fontsize=20)
    # plt.tight_layout()
    # plt.show()

    # plt.figure(figsize=(12,8))
    # plt.boxplot([left_right_result, left_right_result1, left_right_result2, left_right_result3])
    # plt.xticks([1,2,3,4], labels=['현재 신호', 'PSO 1 신호', 'PSO 2 신호', 'PSO 3 신호'], fontsize=20)
    # plt.yticks(fontsize=20)
    # plt.xlabel('학교 -> 정왕역 평균 대기시간 (초)', fontsize=20)
    # plt.ylabel('학교 -> 정왕역 평균 대기시간 (초)', fontsize=20)
    # plt.title('퇴근 시간대 Simulation results of 10 iterations', fontsize=20)
    # plt.tight_layout()
    # plt.show()

    # plt.figure(figsize=(12,8))
    # plt.boxplot([left_right_max_waiting_result, left_right_max_waiting_result1, left_right_max_waiting_result2, left_right_max_waiting_result3])
    # plt.xticks([1,2,3,4,5,6], labels=['현재 신호', 'PSO 1 신호', 'PSO 2 신호', 'PSO 3 신호', 'PSO 4 신호', 'PSO 5 신호'], fontsize=20)
    # plt.yticks(fontsize=20)
    # plt.xlabel('학교 -> 정왕역 최대 대기시간 (초)', fontsize=20)
    # plt.ylabel('학교 -> 정왕역 Max Waiting Time (초)', fontsize=20)
    # plt.title('퇴근 시간대 Simulation results of 10 iterations', fontsize=20)
    # plt.tight_layout()
    # plt.show()

    # plt.figure(figsize=(12,8))
    # plt.boxplot([right_left_result, right_left_result1, right_left_result2, right_left_result3])
    # plt.xticks([1,2,3,4], labels=['현재 신호', 'PSO 1 신호', 'PSO 2 신호', 'PSO 3 신호'], fontsize=20)
    # plt.yticks(fontsize=20)
    # plt.xlabel('학교 <- 정왕역 평균 대기시간 (초)', fontsize=20)
    # plt.ylabel('학교 <- 정왕역 평균 대기시간 (초)', fontsize=20)
    # plt.title('퇴근 시간대 Simulation results of 10 iterations', fontsize=20)
    # plt.tight_layout()
    # plt.show()

    # plt.figure(figsize=(12,8))
    # plt.boxplot([right_left_max_waiting_result, right_left_max_waiting_result1, right_left_max_waiting_result2, right_left_max_waiting_result3])
    # plt.xticks([1,2,3,4,5,6], labels=['현재 신호', 'PSO 1 신호', 'PSO 2 신호', 'PSO 3 신호', 'PSO 4 신호', 'PSO 5 신호'], fontsize=20)
    # plt.yticks(fontsize=20)
    # plt.xlabel('학교 <- 정왕역 최대 대기시간 (초)', fontsize=20)
    # plt.ylabel('학교 <- 정왕역 Max Waiting Time (초)', fontsize=20)
    # plt.title('퇴근 시간대 Simulation results of 10 iterations', fontsize=20)
    # plt.tight_layout()
    # plt.show()

    # plt.figure(figsize=(12,8))
    # plt.boxplot([up_down_result, up_down_result1, up_down_result2, up_down_result3])
    # plt.xticks([1,2,3,4], labels=['현재 신호', 'PSO 1 신호', 'PSO 2 신호', 'PSO 3 신호'], fontsize=20)
    # plt.yticks(fontsize=20)
    # plt.xlabel('학교 <- 정왕역 평균 대기시간 (초)', fontsize=20)
    # plt.ylabel('48 -> 49 평균 대기시간 (초)', fontsize=20)
    # plt.title('퇴근 시간대 Simulation results of 10 iterations', fontsize=20)
    # plt.tight_layout()

    # plt.show()
    # plt.figure(figsize=(12,8))
    # plt.boxplot([down_up_result, down_up_result1, down_up_result2, down_up_result3])
    # plt.xticks([1,2,3,4], labels=['현재 신호', 'PSO 1 신호', 'PSO 2 신호', 'PSO 3 신호'], fontsize=20)
    # plt.yticks(fontsize=20)
    # plt.xlabel('학교 <- 정왕역 평균 대기시간 (초)', fontsize=20)
    # plt.ylabel('48 <- 49 평균 대기시간 (초)', fontsize=20)
    # plt.title('퇴근 시간대 Simulation results of 10 iterations', fontsize=20)
    # plt.tight_layout()
    # plt.show()

    # plt.figure(figsize=(12,8))
    # plt.boxplot([travel_result, travel_result1, travel_result2, travel_result3, travel_result4, travel_result5])
    # plt.xticks([1,2,3,4,5,6], labels=['현재 신호', 'PSO 1 신호', 'PSO 2 신호', 'PSO 3 신호', 'PSO 4 신호', 'PSO 5 신호'], fontsize=20)
    # plt.yticks(fontsize=20)
    # plt.xlabel('평균 이동시간 (초)', fontsize=20)
    # plt.ylabel('Average Moving Time Result (초)', fontsize=20)
    # plt.title('퇴근 시간대 Simulation results of 10 iterations', fontsize=20)
    # plt.tight_layout()
    # plt.show()

    # plt.figure(figsize=(16,10))
    # plt.plot(range(3780, 10801), average_waiting_time_list[180:], linewidth = 3)
    # plt.plot(range(3780, 10801), average_waiting_time_list1[180:], '--', linewidth = 2)
    # plt.plot(range(3780, 10801), average_waiting_time_list2[180:], ':', linewidth = 2)
    # plt.plot(range(3780, 10801), average_waiting_time_list3[180:], '-', linewidth = 3)
    # plt.xticks(fontsize=16)
    # plt.yticks(fontsize=16)
    # plt.legend(['기존 신호', 'PSO 1 신호', 'PSO 2 신호', 'PSO 3 신호'], fontsize=18)
    # plt.xlabel('시간 단계 (초)', fontsize=20)
    # plt.ylabel('평균 대기시간 (초)', fontsize=20)
    # plt.grid(True, linestyle='--', alpha=0.6)
    # plt.tight_layout()
    # plt.show()

    # df = pd.DataFrame([average_waiting_time_list[180:], average_waiting_time_list5[180:]])
    # df.to_csv('시뮬레이션 결과.csv')

if __name__ == "__main__":
    main()
