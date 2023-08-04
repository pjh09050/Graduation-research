import traci

def modify_phase(current_phases0, current_phases1, current_phases2):
    print('current :', current_phases0, current_phases1, current_phases2)
    print('신호주기 합 :', sum(current_phases0), sum(current_phases1), sum(current_phases2))
    # 신호등 ID 가져오기
    traffic_light_id0 = traci.trafficlight.getIDList()[0]
    traffic_light_id1 = traci.trafficlight.getIDList()[1]
    traffic_light_id2 = traci.trafficlight.getIDList()[2]

    new_phases0 = current_phases0
    new_phases1 = current_phases1
    new_phases2 = current_phases2

    ### '00' 신호등 의 모든 phase 정보 가져오기 ###
    complete_definition0 = traci.trafficlight.getCompleteRedYellowGreenDefinition(traffic_light_id0)
    for i, phase in enumerate(complete_definition0[0].phases):
        phase.duration = new_phases0[i]  # new_phases의 duration 값을 할당합니다.
        phase.minDur = new_phases0[i]
        phase.maxDur = new_phases0[i]
    # 수정된 신호등 phase 정보를 시뮬레이터에 적용
    traci.trafficlight.setCompleteRedYellowGreenDefinition(traffic_light_id0, complete_definition0[0])

    ### '000' 신호등 의 모든 phase 정보 가져오기 ###
    complete_definition1 = traci.trafficlight.getCompleteRedYellowGreenDefinition(traffic_light_id1)
    for i, phase in enumerate(complete_definition1[0].phases):
        phase.duration = new_phases1[i]  # new_phases의 duration 값을 할당합니다.
        phase.minDur = new_phases1[i]
        phase.maxDur = new_phases1[i]
    # 수정된 신호등 phase 정보를 시뮬레이터에 적용
    traci.trafficlight.setCompleteRedYellowGreenDefinition(traffic_light_id1, complete_definition1[0])

    ### '0000' 신호등 의 모든 phase 정보 가져오기 ###
    complete_definition2 = traci.trafficlight.getCompleteRedYellowGreenDefinition(traffic_light_id2)
    for i, phase in enumerate(complete_definition2[0].phases):
        phase.duration = new_phases2[i]  # new_phases의 duration 값을 할당합니다.
        phase.minDur = new_phases2[i]
        phase.maxDur = new_phases2[i]
    # 수정된 신호등 phase 정보를 시뮬레이터에 적용
    traci.trafficlight.setCompleteRedYellowGreenDefinition(traffic_light_id2, complete_definition2[0])

    return new_phases0, new_phases1, new_phases2