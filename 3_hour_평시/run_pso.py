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
from PSO_normalized import PSO
import numpy as np

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
            target_score, left_right = calculate_target_index()
            list_cycle.append(target_score)
            average = sum(list_cycle)/len(list_cycle)
            if step % 180 == 0:
                print("{} Average_waiting_time : {:.2f}".format(step, average))
        step += 1
    print("Average_waiting_time: {:.2f}".format(average))
    traci.close()
    return average

result = []
def objective_function(x):
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

    if len(result) % 1000 ==0:
        pd.DataFrame(result).to_csv('result{}.csv'.format(len(result)), header=False, index=False)
    return z

min_dur = [35, 12, 22, 48, 13, 31, 12, 22, 42, 23, 56, 19, 13, 1, 45]
cur_dur = [45, 17, 27, 58, 18, 41, 17, 27, 52, 28, 66, 22, 18, 4, 55]
max_dur = [50, 22, 32, 63, 23, 46, 22, 32, 57, 38, 76, 29, 23, 8, 65]

# pso 결과
pso_dur = []

if __name__ == "__main__":
    bounds = []
    for i in range(len(min_dur)):
        bounds.append((min_dur[i], max_dur[i]))
    num_particles = 20
    maxiter = 100
    pso = PSO(objective_function, bounds, num_particles, maxiter)
    pso.run_result()