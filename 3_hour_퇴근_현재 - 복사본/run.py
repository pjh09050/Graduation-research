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

# $SUMO_HOME/tools directory에서 python module 가져와야 실행 가능
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

all_left_right = ['02to00_0','02to00_1','02to00_2','02to00_3','00toc1_0','00toc1_1','00toc1_2','c1to000_0','c1to000_1','c1to000_2','c1to000_3','000toc4_1','000toc4_2','000toc4_3','c4to0000_0','c4to0000_1','c4to0000_2','c4to0000_3',
                '0000to04_1','0000to04_2','0000to04_3','03to0000_0','03to0000_1','03to0000_2','03to0000_3','0000toc3_0','0000toc3_1','0000toc3_2','c3to000_0','c3to000_1','c3to000_2','c3to000_3','000toc2_0','000toc2_1',
                '000toc2_2','c2to00_0','c2to00_1','c2to00_2','c2to00_3','00to01_0','00to01_1','00to01_2']

def run():
    step = 0
    max_step = 10800
    all_direction_list = []
    right_left_waiting_time = []
    left_right_waiting_time = []
    average_waiting_time_list = []
    
    vehicle_travel_times = {}

    del_lane()

    while step < max_step+1:
        traci.simulationStep()
        step += 1

        if step > 100:
            # vehicle_ids_in_lane = traci.lane.getLastStepVehicleIDs(all_left_right)
            vehicle_ids = traci.vehicle.getIDList()
            for vehicle_id in vehicle_ids:
                if vehicle_id not in vehicle_travel_times:
                    vehicle_travel_times[vehicle_id] = 0
                vehicle_travel_times[vehicle_id] += 1
            average_travel_time_list = list(vehicle_travel_times.values())
            travel_time_average = sum(average_travel_time_list) / len(average_travel_time_list)

            if step > 3600:
                all_direction, right_left, left_right = calculate_target_index()
                all_direction_list.append(all_direction)
                all_direction_average = sum(all_direction_list) / len(all_direction_list)
                average_waiting_time_list.append(all_direction_average)
                            
                right_left_waiting_time.append(right_left)
                right_left_list_average = sum(right_left_waiting_time) / len(right_left_waiting_time)
                
                left_right_waiting_time.append(left_right)
                left_right_list_average = sum(left_right_waiting_time) / len(left_right_waiting_time)
                
                if step % 180 == 0:
                    print("{}초 평균 대기 시간 : {:.2f}".format(step, all_direction_average))
                    print("{}초 학교<-정왕역 평균 대기 시간 : {:.2f}".format(step, right_left_list_average))
                    print("{}초 학교<-정왕역 최대 대기 시간 : {:.2f}".format(step, max(right_left_waiting_time)))
                    print("{}초 학교->정왕역 평균 대기 시간 : {:.2f}".format(step, left_right_list_average))
                    print("{}초 학교->정왕역 최대 대기 시간 : {:.2f}".format(step, max(left_right_waiting_time)))
                    print("{}초 총 이탈 차량 수 : {}, 평균 이동 시간 : {}".format(step, len(vehicle_travel_times), travel_time_average))

    print("평균 대기 시간 : {:.3f}".format(all_direction_average))
    traci.close()
    # plt.plot(range(3780, step), average_waiting_time_list[180:])
    # plt.xlabel('Time Step (단위:분)', fontsize=14)
    # plt.ylabel('Average Waiting Time (단위:분)', fontsize=14)
    # plt.title('출근 시간대 Simulation result', fontsize=16)
    # plt.show()
    return average_waiting_time_list, all_direction_average, left_right_list_average, max(left_right_waiting_time), right_left_list_average, max(left_right_waiting_time), travel_time_average

def main():
    run_step = 0
    waiting_result = []
    left_right_result = []
    left_right_max_waiting_result = []
    right_left_result = []
    right_left_max_waiting_result = []
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
    current_phases3 = [26, 3, 15, 3, 25, 3, 48, 3, 51, 3]
    current_phases4 = [26, 3, 22, 3, 17, 3, 42, 3, 58, 3]
    current_phases5 = [56, 3, 15, 3, 21, 8, 3, 65, 3, 3]
                        
    # 3시간 PSO_정규화_가상 데이터
    # current_phases0 = [27, 3, 16, 3, 23, 3, 53, 3, 46, 3]
    # current_phases1 = [41, 3, 15, 3, 14, 3, 40, 3, 55, 3]
    # current_phases2 = [56, 3, 19, 3, 19, 6, 3, 65, 3, 3]

    # 3시간 PSO_정규화_최종
    # current_phases0 = [26, 3, 23, 3, 23, 3, 46, 3, 47, 3]
    # current_phases1 = [37, 3, 10, 3, 24, 3, 37, 3, 57, 3] 
    # current_phases2 = [60, 3, 20, 3, 13, 2, 3, 70, 3, 3]

    # 3시간 PSO_정규화_찐최종
    # current_phases0 = [23, 3, 20, 3, 21, 3, 42, 3, 59, 3]
    # current_phases1 = [37, 3, 12, 3, 19, 3, 53, 3, 56, 3] 
    # current_phases2 = [56, 3, 18, 3, 21, 8, 3, 62, 3, 3]

    options = False
    if options == False:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    while run_step < 10:
        print('{}번째 시뮬레이션'.format(run_step+1))
        generate_routefile() # 교통량 생성

        # traci를 사용하여 sumo와 python을 연결
        traci.start([sumoBinary, "-c", "new1.sumocfg", "--tripinfo-output", "tripinfo.xml", "--quit-on-end","--start", "--no-warnings"])
        # traci.start([sumoBinary, "-c", "new1.sumocfg", "--tripinfo-output", "tripinfo.xml", "--quit-on-end", "--no-warnings"])
        # sumo에서 신호 세팅해주는 부분
        current_phases0, current_phases1, current_phases2 = modify_phase(current_phases0, current_phases1, current_phases2)

        # sumo 시뮬레이션  성능 추출하는 부분
        average_waiting_time_list, all_direction_average, left_right_list_average, max_waiting_time, right_left_list_average, left_right_waiting_time, average_travel_time = run()

        waiting_result.append(all_direction_average)
        left_right_result.append(left_right_list_average)
        left_right_max_waiting_result.append(max_waiting_time)
        right_left_result.append(right_left_list_average)
        right_left_max_waiting_result.append(left_right_waiting_time)
        travel_result.append(average_travel_time)

        run_step += 1

    run_step = 0
    waiting_result1 = []
    left_right_result1 = []
    left_right_max_waiting_result1 = []
    right_left_result1 = []
    right_left_max_waiting_result1 = []
    travel_result1 = []

    while run_step < 10:
        print('{}번째 시뮬레이션'.format(run_step+1))
        generate_routefile() # 교통량 생성

        # traci를 사용하여 sumo와 python을 연결
        traci.start([sumoBinary, "-c", "new1.sumocfg", "--tripinfo-output", "tripinfo.xml", "--quit-on-end","--start", "--no-warnings"])
        # traci.start([sumoBinary, "-c", "new1.sumocfg", "--tripinfo-output", "tripinfo.xml", "--quit-on-end", "--no-warnings"])
        # sumo에서 신호 세팅해주는 부분
        current_phases3, current_phases4, current_phases5 = modify_phase(current_phases3, current_phases4, current_phases5)

        # sumo 시뮬레이션  성능 추출하는 부분
        average_waiting_time_list1, all_direction_average1, left_right_list_average1, max_waiting_time1, right_left_list_average1, left_right_waiting_time1, average_travel_time1 = run()

        waiting_result1.append(all_direction_average1)
        left_right_result1.append(left_right_list_average1)
        left_right_max_waiting_result1.append(max_waiting_time1)
        right_left_result1.append(right_left_list_average1)
        right_left_max_waiting_result1.append(left_right_waiting_time1)
        travel_result1.append(average_travel_time1)

        run_step += 1

    # print('Average_waiting_time : ', waiting_result)
    # print('{}번 시뮬레이션 : 평균 대기 시간 {:.2f}'.format(run_step, waiting_result_average))
    # print("" "")

    print('waiting_result = ', waiting_result)
    print('waiting_result1 = ', waiting_result1)
    print('left_right_result = ', left_right_result)
    print('left_right_result1 = ', left_right_result1)
    print('left_right_max_waiting_result = ', left_right_max_waiting_result)
    print('left_right_max_waiting_result1 = ', left_right_max_waiting_result1)
    print('right_left_result = ', right_left_result)
    print('right_left_result1 = ', right_left_result1)
    print('right_left_max_waiting_result = ', right_left_max_waiting_result)
    print('right_left_max_waiting_result1 = ', right_left_max_waiting_result1)
    print('travel_result = ', travel_result)
    print('travel_result1 = ', travel_result1)
    
    plt.figure(figsize=(10,8))
    plt.boxplot([waiting_result, waiting_result1])
    plt.xticks([1,2], labels=['현재 신호', 'PSO 신호'], fontsize=14)
    plt.yticks(fontsize=14)
    plt.xlabel('평균 대기시간', fontsize=14)
    plt.ylabel('Average Waiting Time Result (단위:초)', fontsize=14)
    plt.title('퇴근 시간대 Simulation results of 10 iterations', fontsize=16)
    plt.show()

    plt.figure(figsize=(10,8))
    plt.boxplot([left_right_result, left_right_result1])
    plt.xticks([1,2], labels=['현재 신호', 'PSO 신호'], fontsize=14)
    plt.yticks(fontsize=14)
    plt.xlabel('학교 -> 정왕역 평균 대기시간', fontsize=14)
    plt.ylabel('학교 -> 정왕역 Average Waiting Time (단위:초)', fontsize=14)
    plt.title('퇴근 시간대 Simulation results of 10 iterations', fontsize=16)
    plt.show()

    plt.figure(figsize=(10,8))
    plt.boxplot([left_right_max_waiting_result, left_right_max_waiting_result1])
    plt.xticks([1,2], labels=['현재 신호', 'PSO 신호'], fontsize=14)
    plt.yticks(fontsize=14)
    plt.xlabel('학교 -> 정왕역 최대 대기시간', fontsize=14)
    plt.ylabel('학교 -> 정왕역 Max Waiting Time (단위:초)', fontsize=14)
    plt.title('퇴근 시간대 Simulation results of 10 iterations', fontsize=16)
    plt.show()

    plt.figure(figsize=(10,8))
    plt.boxplot([right_left_result, right_left_result1])
    plt.xticks([1,2], labels=['현재 신호', 'PSO 신호'], fontsize=14)
    plt.yticks(fontsize=14)
    plt.xlabel('학교 <- 정왕역 평균 대기시간', fontsize=14)
    plt.ylabel('학교 <- 정왕역 Average Waiting Time (단위:초)', fontsize=14)
    plt.title('퇴근 시간대 Simulation results of 10 iterations', fontsize=16)
    plt.show()

    plt.figure(figsize=(10,8))
    plt.boxplot([right_left_max_waiting_result, right_left_max_waiting_result1])
    plt.xticks([1,2], labels=['현재 신호', 'PSO 신호'], fontsize=14)
    plt.yticks(fontsize=14)
    plt.xlabel('학교 <- 정왕역 최대 대기시간', fontsize=14)
    plt.ylabel('학교 <- 정왕역 Max Waiting Time (단위:초)', fontsize=14)
    plt.title('퇴근 시간대 Simulation results of 10 iterations', fontsize=16)
    plt.show()

    plt.figure(figsize=(10,8))
    plt.boxplot([travel_result, travel_result1])
    plt.xticks([1,2], labels=['현재 신호', 'PSO 신호'], fontsize=14)
    plt.yticks(fontsize=14)
    plt.xlabel('평균 이동시간', fontsize=14)
    plt.ylabel('Average Moving Time Result (단위:초)', fontsize=14)
    plt.title('퇴근 시간대 Simulation results of 10 iterations', fontsize=16)
    plt.show()

    # plt.figure(figsize=(12,8))
    # plt.plot(range(3780, 10801), average_waiting_time_list[180:])
    # plt.plot(range(3780, 10801), average_waiting_time_list1[180:])
    # plt.xticks(fontsize=14)
    # plt.yticks(fontsize=14)
    # plt.legend(['현재 신호', 'PSO 신호'])
    # plt.xlabel('Time Step (단위:분)', fontsize=14)
    # plt.ylabel('Average Waiting Time (단위:초)', fontsize=14)
    # plt.title('퇴근 시간대 Simulation Result', fontsize=16)
    # plt.show()

    # df = pd.DataFrame([result, travel_result])
    # df.to_csv('{}번 시뮬레이션 결과.csv'.format(run_step))

if __name__ == "__main__":
    main()
