import traci

def calculate_target_index():
    # 학교 -> 정왕역 lane list
    left_right = ['02to00_0','02to00_1','02to00_2','02to00_3','00toc1_0','00toc1_1','00toc1_2','c1to000_0','c1to000_1','c1to000_2','c1to000_3','000toc4_1','000toc4_2','000toc4_3','c4to0000_0','c4to0000_1','c4to0000_2','c4to0000_3',
                  '0000to04_1','0000to04_2','0000to04_3','03to0000_0','03to0000_1','03to0000_2','03to0000_3','0000toc3_0','0000toc3_1','0000toc3_2','c3to000_0','c3to000_1','c3to000_2','c3to000_3','000toc2_0','000toc2_1',
                  '000toc2_2','c2to00_0','c2to00_1','c2to00_2','c2to00_3','00to01_0','00to01_1','00to01_2']

    # 49 -> 48 lane list
    up_down = ['1to00_0','1to00_1','1to00_2','1to00_3','00to3_0','00to3_1','00to3_2','4to00_0','4to00_1','4to00_2','4to00_3','00to2_0','00to2_1','00to2_2','5to000_0','5to000_1','000to7_0','000to7_1','8to000_0','8to000_1',
               '000to6_0','000to6_1','9to0000_0','9to0000_1','9to0000_2','9to0000_3','9to0000_4','0000to11_0','0000to11_1','0000to11_2','0000to11_3','12to0000_0','12to0000_1','12to0000_2','12to0000_3','12to0000_4','0000to10_0',
               '0000to10_1','0000to10_2','0000to10_3']

    # 방향별 가중치 넣는 부분
    left_right_ratio = 0.6
    left_right_waiting_times = [traci.lane.getWaitingTime(lane_id) for lane_id in left_right]
    up_down_waiting_times = [traci.lane.getWaitingTime(lane_id) for lane_id in up_down]

    weighted_waiting_times = (left_right_ratio * sum(left_right_waiting_times)) + ((1 - left_right_ratio) * sum(up_down_waiting_times))
    total_lanes = len(left_right) + len(up_down)
    average_waiting_time = weighted_waiting_times / total_lanes

    # 모든 방향 가중치 같게 넣는 부분
    # waiting_times = [traci.lane.getWaitingTime(lane_id) for lane_id in lane_ids]
    # average_waiting_time = sum(waiting_times) / len(waiting_times)

    # 학교 정왕역만 성능 뽑는 부분
    left_right_waiting_times = [traci.lane.getWaitingTime(lane_id) for lane_id in left_right]
    average_left_right_waiting_time = sum(left_right_waiting_times) / len(left_right_waiting_times)
    return average_waiting_time, average_left_right_waiting_time