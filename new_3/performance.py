import traci

def calculate_target_index():
    # 학교 -> 정왕역 lane list
    left_right = []

    # 49 -> 48 lane list
    up_down = []

    # 방향별 가중치 넣는 부분
    left_right_ratio = 0.8
    left_right_waiting_times = [traci.lane.getWaitingTime(lane_id) for lane_id in left_right]
    up_down_waiting_times = [traci.lane.getWaitingTime(lane_id) for lane_id in up_down]

    weighted_waiting_times = (left_right_ratio * sum(left_right_waiting_times)) + ((1 - left_right_ratio) * sum(up_down_waiting_times))
    total_lanes = len(left_right) + len(up_down)
    average_waiting_time = weighted_waiting_times / total_lanes

    # 모든 방향 가중치 같게 넣는 부분
    # waiting_times = [traci.lane.getWaitingTime(lane_id) for lane_id in lane_ids]
    # average_waiting_time = sum(waiting_times) / len(waiting_times)
    return average_waiting_time