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
from PSO import PSO
import numpy as np
import time
import datetime

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

def run():
    step = 0
    max_step = 3600
    list_cycle = []
    average = 0
    del_lane()

    while step < max_step+1:
        traci.simulationStep()
        if step > 600:
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
    y = []
    for num in x:
        y.extend([num, 3])
    print(y)
    x1 = np.array(y[:10])
    x2 = np.array(y[10:20])
    x3 = np.array(y[20:30])
    print(x1)
    print(x2)
    print(x3)
    traci.start([checkBinary('sumo'), "-c", "tt.sumocfg", "--tripinfo-output", "tripinfo.xml", "--quit-on-end","--start", "--no-warnings"])
    modify_phase(x1, x2, x3)
    z =0 
    if sum(x1) != 180:
        z = run()
        return sys.maxsize
    elif sum(x2) != 180:
        z = run()
        return  sys.maxsize
    elif sum(x3) != 180:
        z = run()
        return sys.maxsize
    else:
        z = run()
    result.append([x, z])

    if len(result) % 1000 ==0:
        pd.DataFrame(result).to_csv('result{}.csv'.format(len(result)), header=False, index=False)
    return z


min_dur = [20, 10, 20, 25, 30, 20, 10, 20, 25, 30, 15, 30, 10, 30, 10]
max_dur = [45, 30, 40, 60, 70, 45, 30, 40, 60, 70, 40, 65, 40, 80, 40]

if __name__ == "__main__":

    start = time.time()
    bounds = []
    for i in range(len(min_dur)):
        bounds.append((min_dur[i], max_dur[i]))
    print(bounds)
    num_particles = 30
    maxiter = 1000
    pso = PSO(objective_function, bounds, num_particles, maxiter)
    pso.run_result()
    
    end = time.time()
    sec = end - start
    result_time = datetime.timedelta(seconds=(sec))
    print('총 걸린 시간 : ', result_time)
