import traci

def modify_phase(current_phases0, current_phases1, current_phases2):
    print('current :', current_phases0, current_phases1, current_phases2)
    # 신호등 ID 가져오기
    traffic_light_id0 = traci.trafficlight.getIDList()[0]
    traffic_light_id1 = traci.trafficlight.getIDList()[1]
    traffic_light_id2 = traci.trafficlight.getIDList()[2]
    #print("Traffic light ID:", traffic_light_id)

    new_phases0 = current_phases0
    new_phases1 = current_phases1
    new_phases2 = current_phases2

    ### '00' 신호등 의 모든 phase 정보 가져오기 ###
    complete_definition0 = traci.trafficlight.getCompleteRedYellowGreenDefinition(traffic_light_id0)
    for i, phase in enumerate(complete_definition0[0].phases):
        # print('0 : ', i, phase) # 신호 확인
        phase.duration = new_phases0[i]  # new_phases의 duration 값을 할당합니다.
        phase.minDur = new_phases0[i]
        phase.maxDur = new_phases0[i]
    # 수정된 신호등 phase 정보를 시뮬레이터에 적용
    traci.trafficlight.setCompleteRedYellowGreenDefinition(traffic_light_id0, complete_definition0[0])
    # 수정된 신호등 phase 정보 확인
    modify_phases0 = traci.trafficlight.getCompleteRedYellowGreenDefinition(traffic_light_id0)
    #modify_phases0.phase.duration, modify_phases0.phase.minDur, modify_phases0.phase.maxDur
    #print(modify_phases0[0].phases)

    ### '000' 신호등 의 모든 phase 정보 가져오기 ###
    complete_definition1 = traci.trafficlight.getCompleteRedYellowGreenDefinition(traffic_light_id1)
    for i, phase in enumerate(complete_definition1[0].phases):
        # print('1 : ', i, phase)
        phase.duration = new_phases1[i]  # new_phases의 duration 값을 할당합니다.
        phase.minDur = new_phases1[i]
        phase.maxDur = new_phases1[i]
    # 수정된 신호등 phase 정보를 시뮬레이터에 적용
    traci.trafficlight.setCompleteRedYellowGreenDefinition(traffic_light_id1, complete_definition1[0])
    # 수정된 신호등 phase 정보 확인
    modify_phases1 = traci.trafficlight.getCompleteRedYellowGreenDefinition(traffic_light_id1)
    #print(modify_phases1[0].phases)

    ### '0000' 신호등 의 모든 phase 정보 가져오기 ###
    complete_definition2 = traci.trafficlight.getCompleteRedYellowGreenDefinition(traffic_light_id2)
    for i, phase in enumerate(complete_definition2[0].phases):
        # print('2 : ', i, phase)
        phase.duration = new_phases2[i]  # new_phases의 duration 값을 할당합니다.
        phase.minDur = new_phases2[i]
        phase.maxDur = new_phases2[i]
    # 수정된 신호등 phase 정보를 시뮬레이터에 적용
    traci.trafficlight.setCompleteRedYellowGreenDefinition(traffic_light_id2, complete_definition2[0])
    # 수정된 신호등 phase 정보 확인
    modify_phases2 = traci.trafficlight.getCompleteRedYellowGreenDefinition(traffic_light_id2)
    #print(modify_phases2[0].phases)
    #print('new :', new_phases0, new_phases1, new_phases2)

    return new_phases0, new_phases1, new_phases2