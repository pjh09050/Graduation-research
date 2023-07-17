import traci
from del_lane import del_lane

def calculate_efficiency_index():
    # 대기 시간 추출
    lane_ids = del_lane()

    ## 학교 -> 정왕역 lane list
    left_right = ['0000to000_0', '0000to000_1', '0000to000_2','0000to013_0', '013to014_0', '014to000_0','0000to04_1', '0000to04_2', '0000to04_3','000to0000_1','000to0000_2', '000to0000_3',
    '000to00_0', '000to00_1', '000to00_2','000to011_0','011to012_0', '012to00_0','000to015_0', '015to016_0', '016to0000_0','00to009_0', '009to010_0', '010to000_0', 
    '00to000_0', '00to000_1', '00to000_2', '00to01_0', '00to01_1', '00to01_2', '02to00_0', '02to00_1', '02to00_2', '02to00_3', '03to0000_0', '03to0000_1', '03to0000_2', '03to0000_3']

    ## 49 -> 48 lane list
    up_down = ['0000to10_0', '0000to10_1', '0000to10_2', '0000to10_3','0000to11_0', '0000to11_1', '0000to11_2', '0000to11_3','000to6_0', '000to6_1','000to7_0', '000to7_1', 
    '00to2_0', '00to2_1', '00to2_2', '00to3_0', '00to3_1', '00to3_2', '12to0000_0', '12to0000_1', '12to0000_2', '12to0000_3', '12to0000_4','1to00_0', '1to00_1', '1to00_2', '1to00_3', 
    '4to00_0', '4to00_1', '4to00_2', '4to00_3', '5to000_0', '5to000_1', '8to000_0', '8to000_1', '9to0000_0', '9to0000_1', '9to0000_2', '9to0000_3', '9to0000_4']

    # # 방향별 가중치 넣는 부분
    left_right_ratio = 0.8
    left_right_waiting_times = [traci.lane.getWaitingTime(lane_id) for lane_id in left_right]
    up_down_waiting_times = [traci.lane.getWaitingTime(lane_id) for lane_id in up_down]

    weighted_waiting_times = (left_right_ratio * sum(left_right_waiting_times)) + ((1 - left_right_ratio) * sum(up_down_waiting_times))
    total_lanes = len(left_right) + len(up_down)
    average_waiting_time = weighted_waiting_times / total_lanes

    #print(average_waiting_time)

    # 모든 방향 가중치 같게 넣는 부분
    # waiting_times = [traci.lane.getWaitingTime(lane_id) for lane_id in lane_ids]
    # average_waiting_time = sum(waiting_times) / len(waiting_times)

    # 대기 차량 비율 추출
    # waiting_vehicle_count = sum([traci.lane.getLastStepHaltingNumber(lane_id) for lane_id in lane_ids])
    # total_vehicle_count = sum([traci.lane.getLastStepVehicleNumber(lane_id) for lane_id in lane_ids])
    # waiting_vehicle_ratio = waiting_vehicle_count / total_vehicle_count

    # 통과 차량 비율 추출
    # passing_vehicle_count = total_vehicle_count - waiting_vehicle_count
    # passing_vehicle_ratio = passing_vehicle_count / total_vehicle_count

    # 효율성 지수 계산
    # scaled_waiting_time = average_waiting_time / max(waiting_times)
    # efficiency_index = passing_vehicle_ratio / (scaled_waiting_time + waiting_vehicle_ratio)
    # efficiency_index = passing_vehicle_ratio /  waiting_vehicle_ratio

    # return efficiency_index
    return average_waiting_time
