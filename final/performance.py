import traci

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
    #efficiency_index = passing_vehicle_ratio / (scaled_waiting_time + waiting_vehicle_ratio)
    efficiency_index = passing_vehicle_ratio /  waiting_vehicle_ratio

    return efficiency_index

# SUMO 초기화 및 교통 시뮬레이션 실행
traci.start(['sumo', '-c', 'path/to/your/sumo_config_file.sumocfg'])
traci.simulationStep()

# 효율성 지수 계산
efficiency_index = calculate_efficiency_index()
print("Efficiency Index:", efficiency_index)

# SUMO 종료
traci.close()
