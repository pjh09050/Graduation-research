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
        if step > 1800:
            target_score = calculate_target_index()
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
    y = [num for num in x[:11] for num in (num, 3)]
    y.extend(x[11:12])
    y += [num for num in x[12:] for num in (num, 3)]
    y.extend([3])
    x1 = np.array(y[:10])
    x2 = np.array(y[10:20])
    x3 = np.array(y[20:30])
    traci.start([checkBinary('sumo'), "-c", "new.sumocfg", "--tripinfo-output", "tripinfo.xml", "--quit-on-end", "--start", "--no-warnings"])
    modify_phase(x1, x2, x3)
    z = run()
    result.append([x, z])

    if len(result) % 400 ==0:
        pd.DataFrame(result).to_csv('result{}.csv'.format(len(result)), header=False, index=False)
    return z

min_dur = [25, 12, 42, 28, 15, 25, 12, 60, 25, 15, 42, 20, 13, 20, 41]
cur_dur = [35, 20, 52, 38, 20, 33, 15, 65, 32, 20, 47, 25, 18, 24, 51]
max_dur = [43, 22, 62, 48, 25, 41, 18, 75, 42, 25, 57, 30, 21, 30, 61]

# pso 결과
pso_dur = []

if __name__ == "__main__":
    bounds = []
    for i in range(len(min_dur)):
        bounds.append((min_dur[i], max_dur[i]))
    num_particles = 15
    maxiter = 100
    pso = PSO(objective_function, bounds, num_particles, maxiter)
    pso.run_result()