import numpy as np
import random

def total_traffic():
    np.random.seed(1234)
    total_list = []
    sorted_list = []
    W1_arrival_rate = 1500 / 3600  # 차량 도착율 계산
    W1_time_list = [] # W1 등장 차량 시간 리스트
    W1_arrival_intervals = np.random.exponential(scale=1/W1_arrival_rate, size=1500)
    W1_cumulative_interval = 0
    for i, interval in enumerate(W1_arrival_intervals):
        # W1출발부터 모든 경로에 대한 확률 가중치 부여 후 경로 선택
        car_direction = random.choices(population=["routeW1_N1", "routeW1_S1", "routeW1_N2", "routeW1_S2", "routeW1_S3", "routeW1_E3"], weights=[0.1, 0.1, 0.08, 0.05, 0.07, 0.6], k=1)[0]
        W1_cumulative_interval += interval
        if W1_cumulative_interval > 3600:
            break
        if car_direction == "routeW1_N1":
            departLane = 3
            arrivalLane = 2
        elif car_direction == "routeW1_S1":
            departLane= 0
            arrivalLane = random.randint(0,1)
        elif car_direction == "routeW1_N2":
            departLane = random.randint(1,2)
            arrivalLane = random.randint(0,1)
        elif car_direction == "routeW1_S2":
            departLane = random.randint(1,2)
            arrivalLane = random.randint(0,1)
        elif car_direction == "routeW1_S3":
            departLane = random.randint(1,2)
            arrivalLane = 0
        elif car_direction == "routeW1_E3":
            a = random.random()
            if a < 0.8:
                departLane = random.randint(1,2)
            else:
                departLane = random.randint(0,2)
            arrivalLane = random.randint(1,3)
        W1_time_list.append((car_direction, np.round(W1_cumulative_interval,1), departLane, arrivalLane))

    N1_arrival_rate = 455 / 3600  # 차량 도착율 계산
    N1_time_list = [] # N1 차량 등장 시간 리스트
    N1_arrival_intervals = np.random.exponential(scale=1/N1_arrival_rate, size=455)
    N1_cumulative_interval = 0
    for i, interval in enumerate(N1_arrival_intervals):
        car_direction = random.choices(population=["routeN1_W1", "routeN1_S1", "routeN1_S2", "routeN1_S3", "routeN1_E3"], weights=[0.1, 0.6, 0.08, 0.12, 0.1], k=1)[0]
        N1_cumulative_interval += interval
        if N1_cumulative_interval > 3600:
            break
        if car_direction == "routeN1_W1":
            departLane = 0
            arrivalLane = random.randint(0,1)
        elif car_direction == "routeN1_S1":
            a = random.random()
            if a < 0.8:
                departLane = random.randint(1,2)
            else:
                departLane = random.randint(0,2)
            arrivalLane = random.randint(0,2)
        elif car_direction == "routeN1_S2":
            departLane = 3
            arrivalLane = random.randint(0,1)
        elif car_direction == "routeN1_S3":
            departLane = 3
            arrivalLane = 0
        elif car_direction == "routeN1_E3":
            departLane = 3
            arrivalLane = random.randint(2,3)
        N1_time_list.append((car_direction, np.round(N1_cumulative_interval,1), departLane, arrivalLane))

    S1_arrival_rate = 358 / 3600  # 차량 도착율 계산
    S1_time_list = []
    S1_arrival_intervals = np.random.exponential(scale=1/S1_arrival_rate, size=358)
    S1_cumulative_interval = 0
    for i, interval in enumerate(S1_arrival_intervals):
        car_direction = random.choices(population=["routeS1_W1", "routeS1_N1", "routeS1_S3", "routeS1_E3"], weights=[0.1, 0.7, 0.05, 0.15], k=1)[0]
        S1_cumulative_interval += interval
        if S1_cumulative_interval > 3600:
            break
        if car_direction == "routeS1_W1":
            departLane = 3
            arrivalLane = 2
        elif car_direction == "routeS1_N1":
            a = random.random()
            if a < 0.8:
                departLane = random.randint(1,2)
            else:
                departLane = random.randint(0,1)
            arrivalLane = random.randint(0,2) 
        elif car_direction == "routeS1_S3":
            departLane = 0
            arrivalLane = random.randint(0,1)
        elif car_direction == "routeS1_E3":
            departLane = 0
            arrivalLane = random.randint(1,2)
        S1_time_list.append((car_direction, np.round(S1_cumulative_interval,1), departLane, arrivalLane))

    N2_arrival_rate = 128 / 3600  # 차량 도착율 계산
    N2_time_list = []
    N2_arrival_intervals = np.random.exponential(scale=1/N2_arrival_rate, size=128)
    N2_cumulative_interval = 0
    for i, interval in enumerate(N2_arrival_intervals):
        car_direction = random.choices(population=["routeN2_W1", "routeN2_S1", "routeN2_S2", "routeN2_S3", "routeN2_E3"], weights=[0.1, 0.05, 0.7, 0.05, 0.1], k=1)[0]
        N2_cumulative_interval += interval
        if N2_cumulative_interval > 3600:
            break
        if car_direction == "routeN2_W1":
            departLane = 0
            arrivalLane = 0
        elif car_direction == "routeN2_S1":
            departLane= 0
            arrivalLane = random.randint(1,2)
        elif car_direction == "routeN2_S2":
            a = random.random()
            if a < 0.6:
                departLane = 1
                arrivalLane = 1
            else:
                departLane = 0
                arrivalLane = 0
        elif car_direction == "routeN2_S3":
            departLane = 1
            arrivalLane = 0
        elif car_direction == "routeN2_E3":
            departLane = 1
            arrivalLane = random.randint(2,3)
        N2_time_list.append((car_direction, np.round(N2_cumulative_interval,1), departLane, arrivalLane))

    S2_arrival_rate = 153 / 3600  # 차량 도착율 계산
    S2_time_list = []
    S2_arrival_intervals = np.random.exponential(scale=1/S2_arrival_rate, size=153)
    S2_cumulative_interval = 0
    for i, interval in enumerate(S2_arrival_intervals):
        car_direction = random.choices(population=["routeS2_W1", "routeS2_N1", "routeS2_N2", "routeS2_S3", "routeS2_E3"], weights=[0.08, 0.07, 0.65, 0.05, 0.15], k=1)[0]
        S2_cumulative_interval += interval
        if S2_cumulative_interval > 3600:
            break
        if car_direction == "routeS2_W1":
            departLane = 1
            arrivalLane = random.randint(1,2)
        elif car_direction == "routeS2_N1":
            departLane= 1
            arrivalLane = 0
        elif car_direction == "routeS2_N2":
            a = random.random()
            if a < 0.6:
                departLane = 1
                arrivalLane = 1
            else:
                departLane = 0
                arrivalLane = 0
        elif car_direction == "routeS2_S3":
            departLane = 0
            arrivalLane = 0
        elif car_direction == "routeS2_E3":
            departLane = 0
            arrivalLane = random.randint(1,2)
        S2_time_list.append((car_direction, np.round(S2_cumulative_interval,1), departLane, arrivalLane))

    N3_arrival_rate = 1147 / 3600  # 차량 도착율 계산
    N3_time_list = []
    N3_arrival_intervals = np.random.exponential(scale=1/N3_arrival_rate, size=1147)
    N3_cumulative_interval = 0
    for i, interval in enumerate(N3_arrival_intervals):
        car_direction = random.choices(population=["routeN3_W1", "routeN3_N1", "routeN3_S1", "routeN3_S2", "routeN3_S3", "routeN3_E3"], weights=[0.1, 0.07, 0.06, 0.07, 0.65, 0.05], k=1)[0]
        N3_cumulative_interval += interval
        if N3_cumulative_interval > 3600:
            break
        if car_direction == "routeN3_W1":
            departLane = 0
            arrivalLane = random.randint(1,2)
        elif car_direction == "routeN3_N1":
            departLane= 0
            arrivalLane = 0
        elif car_direction == "routeN3_S1":
            departLane = 0
            arrivalLane = random.randint(1,2)
        elif car_direction == "routeN3_S2":
            departLane = 0
            arrivalLane = random.randint(0,1)
        elif car_direction == "routeN3_S3":
            a = random.random()
            if a < 0.8:
                departLane = random.randint(1,3)
            else:
                departLane = random.randint(0,3)
            arrivalLane = random.randint(1,3) 
        elif car_direction == "routeN3_E3":
            departLane = 4
            arrivalLane = 2
        N3_time_list.append((car_direction, np.round(N3_cumulative_interval,1), departLane, arrivalLane))

    S3_arrival_rate = 1881 / 3600  # 차량 도착율 계산
    S3_time_list = []
    S3_arrival_intervals = np.random.exponential(scale=1/S3_arrival_rate, size=1881)
    S3_cumulative_interval = 0
    for i, interval in enumerate(S3_arrival_intervals):
        car_direction = random.choices(population=["routeS3_W1", "routeS3_N1", "routeS3_S1", "routeS3_N2", "routeS3_N3", "routeS3_E3"], weights=[0.03, 0.07, 0.16, 0.07, 0.55, 0.12], k=1)[0]
        S3_cumulative_interval += interval
        if S3_cumulative_interval > 3600:
            break
        if car_direction == "routeS3_W1":
            departLane = 4
            arrivalLane = random.randint(1,2)
        elif car_direction == "routeS3_N1":
            departLane= 4
            arrivalLane = random.randint(0,1)
        elif car_direction == "routeS3_S1":
            departLane = 4
            arrivalLane = random.randint(1,2)
        elif car_direction == "routeS3_N2":
            departLane = 4
            arrivalLane = random.randint(0,1)
        elif car_direction == "routeS3_N3":
            a = random.random()
            if a < 0.8:
                departLane = random.randint(1,3)
            else:
                departLane = random.randint(0,3)
            arrivalLane = random.randint(0,3) 
        elif car_direction == "routeS3_E3":
            departLane = 0
            arrivalLane = 1
        S3_time_list.append((car_direction, np.round(S3_cumulative_interval,1), departLane, arrivalLane))
    
    E3_arrival_rate = 720 / 3600  # 차량 도착율 계산
    E3_time_list = []
    E3_arrival_intervals = np.random.exponential(scale=1/E3_arrival_rate, size=720)
    E3_cumulative_interval = 0
    for i, interval in enumerate(E3_arrival_intervals):
        car_direction = random.choices(population=["routeE3_W1", "routeE3_N1", "routeE3_S1", "routeE3_N2", "routeE3_S2", "routeE3_N3", "routeE3_S3"], weights=[0.52, 0.06, 0.09, 0.07, 0.1, 0.07, 0.09], k=1)[0]
        E3_cumulative_interval += interval
        if E3_cumulative_interval > 3600:
            break
        if car_direction == "routeE3_W1":
            a = random.random()
            if a < 0.8:
                departLane = random.randint(1,2)
            else:
                departLane = random.randint(0,2)
            arrivalLane = random.randint(0,2) 
        elif car_direction == "routeE3_N1":
            departLane= random.randint(0,2)
            arrivalLane = 0
        elif car_direction == "routeE3_S1":
            departLane = random.randint(1,2)
            arrivalLane = random.randint(0,1)
        elif car_direction == "routeE3_N2":
            departLane = 0
            arrivalLane = random.randint(0,1)
        elif car_direction == "routeE3_S2":
            departLane = 2
            arrivalLane = random.randint(0,1)
        elif car_direction == "routeE3_N3":
            departLane = 0
            arrivalLane = 0
        elif car_direction == "routeE3_S3":
            departLane = 3
            arrivalLane = random.randint(2,3)
        E3_time_list.append((car_direction, np.round(E3_cumulative_interval,1), departLane, arrivalLane))

    total_list = W1_time_list + N1_time_list + S1_time_list + N2_time_list + S2_time_list + N3_time_list + S3_time_list + E3_time_list
    sorted_list = sorted(total_list, key=lambda x: x[1])
    print(len(sorted_list))
    print(sorted_list[6233])

    return sorted_list