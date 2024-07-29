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
from performance import calculate_target_index
from Discrete_PSO import PSO
import numpy as np
import time

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")


def run():
    step = 0
    max_step = 10800
    list_cycle = []
    average = 0
    del_lane()
    while step < max_step+1:
        traci.simulationStep()
        if step > 3600:
            start_time = time.time()
            target_score, right_left, left_right, up_down, down_up = calculate_target_index()
            list_cycle.append(target_score)
            average = sum(list_cycle)/len(list_cycle)
            if step % 180 == 0:
                print("{} Average_waiting_time : {:.2f}".format(step, average))
            end_time = time.time()
            print('단위 스텝(Sec): ', end_time-start_time)
        step += 1
    print("Average_waiting_time: {:.2f}".format(average))
    traci.close()

    return average

result = []
def objective_function(x):
    start_time = time.time()  # 시작 시간 기록
    generate_routefile()
    y = [num for num in x[:12] for num in (num, 3)]
    y.extend(x[12:13])
    y += [num for num in x[13:] for num in (num, 3)]
    y.extend([3])
    x1 = np.array(y[:10])
    x2 = np.array(y[10:20])
    x3 = np.array(y[20:30])
    traci.start([checkBinary('sumo'), "-c", "new1.sumocfg", "--tripinfo-output", "tripinfo.xml", "--quit-on-end", "--start", "--no-warnings"])
    modify_phase(x1, x2, x3)
    z = run()
    result.append([x, z])
    end_time = time.time()  # 종료 시간 기록
    elapsed_time = end_time - start_time
    print(f"Execution time: {elapsed_time} seconds")

    if len(result) % 1000 ==0:
        pd.DataFrame(result).to_csv('result{}.csv'.format(len(result)), header=False, index=False)
    return z

min_dur = [25, 12, 22, 28, 42, 25, 12, 15, 30, 51, 56, 19, 13, 1, 45]
cur_dur = [31, 17, 27, 38, 52, 33, 17, 22, 32, 61, 66, 22, 18, 4, 55]
max_dur = [41, 22, 32, 48, 62, 43, 22, 27, 42, 65, 76, 29, 23, 8, 65]


if __name__ == "__main__":
    bounds = []
    for i in range(len(min_dur)):
        bounds.append((min_dur[i], max_dur[i]))
    num_particles = 10
    maxiter = 10
    best_pick = 5
    start_time = time.time()  # 시작 시간 기록
    pso = PSO(objective_function, bounds, num_particles, maxiter, best_pick)
    pso.run_result()
    end_time = time.time()  # 종료 시간 기록

    elapsed_time = end_time - start_time
    print(f"Execution time: {elapsed_time} seconds")