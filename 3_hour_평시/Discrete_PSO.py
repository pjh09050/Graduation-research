import random
from math import *
import sys
import os
from sumolib import checkBinary  
import traci
from TrafficGenerator import generate_routefile
from modify_phase import modify_phase
from del_lane import del_lane
from performance import calculate_target_index
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
            target_score, right_left, left_right, up_down, down_up = calculate_target_index()
            list_cycle.append(target_score)
            average = sum(list_cycle)/len(list_cycle)
            if step % 180 == 0:
                print("{} Average_waiting_time : {:.2f}".format(step, average))
        step += 1
    print("Average_waiting_time: {:.2f}".format(average))
    traci.close()
    return average

def main(x):
    run_step = 0
    waiting_result = []

    options = True
    if options == False:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    y = [num for num in x[:12] for num in (num, 3)]
    y.extend(x[12:13])
    y += [num for num in x[13:] for num in (num, 3)]
    y.extend([3])
    current_phases0 = np.array(y[:10])
    current_phases1 = np.array(y[10:20])
    current_phases2 = np.array(y[20:30])

    while run_step < 10:
        generate_routefile()
        traci.start([sumoBinary, "-c", "new1.sumocfg", "--tripinfo-output", "tripinfo.xml", "--quit-on-end","--start", "--no-warnings"])
        current_phases0, current_phases1, current_phases2 = modify_phase(current_phases0, current_phases1, current_phases2)
        average= run()
        waiting_result.append(average)
        run_step += 1
    waiting_result_average = sum(waiting_result) / len(waiting_result)
    return waiting_result_average

class Particle:
    def __init__(self, bounds, max_iter):
        self.position = []  # particle current position
        self.velocity = []  # particle current velocity
        self.best_position = [] # particle best position
        self.fitness = sys.maxsize   # particle fitness
        self.best_fitness = sys.maxsize  # particle best fitness
        self.iteration = 0 # 반복 횟수
        self.max_iter = max_iter
        for i in range(len(bounds)):
            self.position.append((random.uniform(bounds[i][0], bounds[i][1])))
            self.velocity.append(random.uniform(-1, 1))

        x1 = self.position[:5]
        x2 = self.position[5:10]
        x3 = self.position[10:]
        x1_sum = sum(x1)
        x2_sum = sum(x2)
        x3_sum = sum(x3)
        x1_normalized = [x / x1_sum for x in x1]
        x1_adjusted = [int(x * 165) for x in x1_normalized]
        x2_normalized = [x / x2_sum for x in x2]
        x2_adjusted = [int(x * 165) for x in x2_normalized]
        x3_normalized = [x / x3_sum for x in x3]
        x3_adjusted = [int(x * 165) for x in x3_normalized]
        self.position = x1_adjusted + x2_adjusted + x3_adjusted

        while True: # 합이 495될때까지 반복
            x1_sum = int(round(sum(self.position[:5])))
            x2_sum = int(round(sum(self.position[5:10])))
            x3_sum = int(round(sum(self.position[10:])))
            if x1_sum == 165 and x2_sum == 165 and x3_sum == 165:
                break
            if x1_sum > 165:
                minus_list = [1,0,2,3,4]
                for i in range(abs(x1_sum - 165)):
                    if int(round(sum(self.position[:5]))) == 165:
                        break
                    idx = i % len(minus_list)
                    position_idx = minus_list[idx]
                    self.position[position_idx] -= 1
                    self.position[position_idx] = int(round(self.position[position_idx]))
            else:
                plus_list = [4,3,2,0,1]
                for i in range(abs(x1_sum - 165)):
                    if int(round(sum(self.position[:5]))) == 165:
                        break
                    idx = i % len(plus_list)
                    position_idx = plus_list[idx]
                    self.position[position_idx] += 1
                    self.position[position_idx] = int(round(self.position[position_idx]))

            if x2_sum > 165:
                minus_list = [1,0,2,3,4]
                for i in range(abs(x2_sum - 165)):
                    if int(round(sum(self.position[5:10]))) == 165:
                        break
                    idx = i % len(minus_list)
                    position_idx = minus_list[idx] + 5
                    self.position[position_idx] -= 1
                    self.position[position_idx] = int(round(self.position[position_idx]))
            else:
                plus_list = [4,3,2,0,1]
                for i in range(abs(x2_sum - 165)):
                    if int(round(sum(self.position[5:10]))) == 165:
                        break
                    idx = i % len(plus_list)
                    position_idx = plus_list[idx] + 5
                    self.position[position_idx] += 1
                    self.position[position_idx] = int(round(self.position[position_idx]))

            if x3_sum > 165:
                minus_list = [2,1,0,3,4]
                for i in range(abs(x3_sum - 165)):
                    if int(round(sum(self.position[10:]))) == 165:
                        break
                    idx = i % len(minus_list)
                    position_idx = minus_list[idx] + 10
                    self.position[position_idx] -= 1
                    self.position[position_idx] = int(round(self.position[position_idx]))
                    if self.position[position_idx] < 0 and position_idx < 14:
                        self.position[position_idx] += 1
                        self.position[position_idx] = int(round(self.position[position_idx]))
                        position_idx += 1
            else:
                plus_list = [4,3,0,1,2]
                for i in range(abs(x3_sum - 165)):
                    if int(round(sum(self.position[10:]))) == 165:
                        break
                    idx = i % len(plus_list)
                    position_idx = plus_list[idx] + 10
                    self.position[position_idx] += 1
                    self.position[position_idx] = int(round(self.position[position_idx]))
                    if self.position[position_idx] < 0 and position_idx < 14:
                        self.position[position_idx] += 1
                        self.position[position_idx] = int(round(self.position[position_idx]))
                        position_idx += 1

    def evaluate_fitness(self, fitness_func):
        # current position에 대한 fitness 계산
        self.fitness = fitness_func(self.position)
        # best_position과 best_fitness 업데이트
        if self.fitness < self.best_fitness:
            self.best_position = self.position
            self.best_fitness = self.fitness

    def update_velocity(self, global_best_position):
        w_min = 0.5
        w_max = 1
        self.iteration += 1
        w = w_max - ((w_max - w_min) * self.iteration / self.max_iter) # w가 점점 감소
        c1 = 1  # 자신의 최고 위치에 대한 가중치
        c2 = 2  # 집단의 최고 위치에 대한 가중치
        threshold = random.random()  # 임의의 threshold 값
        for i in range(len(self.position)):
            r1 = random.random() # 0,1 사이의 난수
            r2 = random.random()
            cognitive_velocity = c1 * r1 * (self.best_position[i] - self.position[i])
            social_velocity = c2 * r2 * (global_best_position[i] - self.position[i])
            self.velocity[i] = w * self.velocity[i] + cognitive_velocity + social_velocity
            # threshold를 기준으로 반올림 또는 반내림
            if threshold > 0.3:
                self.velocity[i] = int(round(self.velocity[i]))
            else:
                self.velocity[i] = int(self.velocity[i])
        # self.velocity = [int(round(v)) for v in self.velocity]

    def update_position(self, bounds):
        for i in range(len(self.position)):
            self.position[i] = self.position[i] + self.velocity[i]
            self.position[i] = round(self.position[i], 1)
            # adjust maximum position 
            if self.position[i] < bounds[i][0]:
                self.position[i] = bounds[i][0]
            # adjust minimum position 
            elif self.position[i] > bounds[i][1]:
                self.position[i] = bounds[i][1]
        x1 = self.position[:5]
        x2 = self.position[5:10]
        x3 = self.position[10:]
        x1_sum = sum(x1)
        x2_sum = sum(x2)
        x3_sum = sum(x3)
        x1_normalized = [x / x1_sum for x in x1]
        x1_adjusted = [int(x * 165) for x in x1_normalized]
        x2_normalized = [x / x2_sum for x in x2]
        x2_adjusted = [int(x * 165) for x in x2_normalized]
        x3_normalized = [x / x3_sum for x in x3]
        x3_adjusted = [int(x * 165) for x in x3_normalized]
        self.position = x1_adjusted + x2_adjusted + x3_adjusted

        while True: # 합이 495될때까지 반복
            x1_sum = int(round(sum(self.position[:5])))
            x2_sum = int(round(sum(self.position[5:10])))
            x3_sum = int(round(sum(self.position[10:])))
            if x1_sum == 165 and x2_sum == 165 and x3_sum == 165:
                break
            if x1_sum > 165:
                minus_list = [1,0,2,3,4]
                for i in range(abs(x1_sum - 165)):
                    if int(round(sum(self.position[:5]))) == 165:
                        break
                    idx = i % len(minus_list)
                    position_idx = minus_list[idx]
                    self.position[position_idx] -= 1
                    self.position[position_idx] = int(round(self.position[position_idx]))
            else:
                plus_list = [4,3,2,0,1]
                for i in range(abs(x1_sum - 165)):
                    if int(round(sum(self.position[:5]))) == 165:
                        break
                    idx = i % len(plus_list)
                    position_idx = plus_list[idx]
                    self.position[position_idx] += 1
                    self.position[position_idx] = int(round(self.position[position_idx]))

            if x2_sum > 165:
                minus_list = [1,0,2,3,4]
                for i in range(abs(x2_sum - 165)):
                    if int(round(sum(self.position[5:10]))) == 165:
                        break
                    idx = i % len(minus_list)
                    position_idx = minus_list[idx] + 5
                    self.position[position_idx] -= 1
                    self.position[position_idx] = int(round(self.position[position_idx]))
            else:
                plus_list = [4,3,2,0,1]
                for i in range(abs(x2_sum - 165)):
                    if int(round(sum(self.position[5:10]))) == 165:
                        break
                    idx = i % len(plus_list)
                    position_idx = plus_list[idx] + 5
                    self.position[position_idx] += 1
                    self.position[position_idx] = int(round(self.position[position_idx]))

            if x3_sum > 165:
                minus_list = [2,1,0,3,4]
                for i in range(abs(x3_sum - 165)):
                    if int(round(sum(self.position[10:]))) == 165:
                        break
                    idx = i % len(minus_list)
                    position_idx = minus_list[idx] + 10
                    self.position[position_idx] -= 1
                    self.position[position_idx] = int(round(self.position[position_idx]))
                    if self.position[position_idx] < 0 and position_idx < 14:
                        self.position[position_idx] += 1
                        self.position[position_idx] = int(round(self.position[position_idx]))
                        position_idx += 1
            else:
                plus_list = [4,3,0,1,2]
                for i in range(abs(x3_sum - 165)):
                    if int(round(sum(self.position[10:]))) == 165:
                        break
                    idx = i % len(plus_list)
                    position_idx = plus_list[idx] + 10
                    self.position[position_idx] += 1
                    self.position[position_idx] = int(round(self.position[position_idx]))
                    if self.position[position_idx] < 0 and position_idx < 14:
                        self.position[position_idx] += 1
                        self.position[position_idx] = int(round(self.position[position_idx]))
                        position_idx += 1

class PSO:
    def __init__(self, fitness_function, bounds, num_particles, max_iter, best_pick):
        self.fitness_func = fitness_function
        self.bounds = bounds
        self.num_particles = num_particles
        self.max_iter = max_iter
        self.best_pick = best_pick
        self.global_best_position = []  # group best position
        self.discrete_pso = []
        self.global_best_fitness = -1  # group best fitness
        self.swarm = [] # 초기 particles
        self.result = []
        for i in range(num_particles):
            self.swarm.append(Particle(bounds, self.max_iter))
            
    def run_result(self):
        for i in range(self.max_iter):
            # 각 particle의 fitness 평가하기
            for j in range(self.num_particles):
                self.swarm[j].evaluate_fitness(self.fitness_func)
                # global_best_position, global_best_fitness 업데이트
                if self.swarm[j].fitness < self.global_best_fitness or self.global_best_fitness == -1:
                    self.global_best_position = list(self.swarm[j].position)
                    self.discrete_pso.append(self.global_best_position)
                    self.global_best_fitness = float(self.swarm[j].fitness)
            # 각 particle의 position과 velocity 업데이트
            for j in range(self.num_particles):
                self.swarm[j].update_velocity(self.global_best_position)
                self.swarm[j].update_position(self.bounds)

        # print('discrete pso:', self.discrete_pso)
        self.min_i = None 
        self.min_z = float('inf')
        for i in self.discrete_pso[-self.best_pick:]:
            z = main(i)
            self.result.append([i, z])
            for i, z in self.result:
                if z < self.min_z:
                    self.min_i = i
                    self.min_z = z
        print('discrete pso:', self.discrete_pso)
        print('z :', [self.min_i, self.min_z])
        # print('Best position:', self.global_best_position)
        print('sum best position', sum(self.global_best_position))
        print('Best fitness:', self.global_best_fitness)
        return self.global_best_position, self.global_best_fitness