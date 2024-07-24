import random
import sys
import os
import numpy as np
import time
import pandas as pd
from sumolib import checkBinary  
import traci
from TrafficGenerator import generate_routefile
from modify_phase import modify_phase
from del_lane import del_lane
from performance import calculate_target_index
from tqdm import tqdm

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
    while step < max_step + 1:
        traci.simulationStep()
        if step > 3600:
            target_score, right_left, left_right, up_down, down_up = calculate_target_index()
            list_cycle.append(target_score)
            average = sum(list_cycle) / len(list_cycle)
            if step % 180 == 0:
                print("{} Average_waiting_time : {:.2f}".format(step, average))
        step += 1
    print("Average_waiting_time: {:.2f}".format(average))
    traci.close()
    return average

class Ant:
    def __init__(self, bounds, interval_size, node_number):
        self.bounds = bounds
        self.position = []
        self.fitness = sys.maxsize
        for i in range(len(bounds)):
            min_bound, max_bound = bounds[i]
            node_number = int(interval_size[i]) + 1
            num_node = random.randint(1, node_number)
            g = (min_bound - interval_size[i]) + (num_node * interval_size[i])
            g = max(min(g, max_bound), min_bound)
            self.position.append(g)
        self.position = self.normalize_position(self.position)
        print(self.position)
    
    def normalize_position(self, position):
        x1 = position[:5]
        x2 = position[5:10]
        x3 = position[10:]
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
        self.adjust_position()
        return self.position

    def adjust_position(self):
        while True:  # 합이 495 될 때까지 반복
            x1_sum = int(round(sum(self.position[:5])))
            x2_sum = int(round(sum(self.position[5:10])))
            x3_sum = int(round(sum(self.position[10:])))
            if x1_sum == 165 and x2_sum == 165 and x3_sum == 165:
                break
            if x1_sum != 165:
                self.correct_segment(self.position[:5], 0, 165)
            if x2_sum != 165:
                self.correct_segment(self.position[5:10], 5, 165)
            if x3_sum != 165:
                self.correct_segment(self.position[10:], 10, 165)

    # def correct_segment(self, segment, offset, target_sum):
    #     segment_sum = int(round(sum(segment)))
    #     if segment_sum > target_sum:
    #         minus_list = [1, 0, 2, 3, 4]
    #         for i in range(abs(segment_sum - target_sum)):
    #             if int(round(sum(segment))) == target_sum:
    #                 break
    #             idx = i % len(minus_list)
    #             position_idx = minus_list[idx] + offset
    #             self.position[position_idx] -= 1
    #             self.position[position_idx] = int(round(self.position[position_idx]))
    #     else:
    #         plus_list = [4, 3, 2, 0, 1]
    #         for i in range(abs(segment_sum - target_sum)):
    #             if int(round(sum(segment))) == target_sum:
    #                 break
    #             idx = i % len(plus_list)
    #             position_idx = plus_list[idx] + offset
    #             self.position[position_idx] += 1
    #             self.position[position_idx] = int(round(self.position[position_idx]))

    def correct_segment(self, segment, offset, target_sum):
        bounds = self.bounds[offset:offset + len(segment)]
        min_bound = [b[0] for b in bounds]
        max_bound = [b[1] for b in bounds]
        segment_sum = int(round(sum(segment)))
    
        if segment_sum > target_sum:
            minus_list = [1, 0, 2, 3, 4]
            print(abs(segment_sum - target_sum))
            for i in range(abs(segment_sum - target_sum)+100):
                if int(round(sum(segment))) == target_sum:
                    break
                idx = i % len(minus_list)
                position_idx = minus_list[idx]
                segment[position_idx] -= 1
                if segment[position_idx] < min_bound[position_idx]:
                    segment[position_idx] = min_bound[position_idx]
                segment_sum = int(round(sum(segment)))
        else:
            plus_list = [4, 3, 2, 0, 1]
            for i in range(abs(segment_sum - target_sum)+ 100):
                if int(round(sum(segment))) == target_sum:
                    break
                idx = i % len(plus_list)
                position_idx = plus_list[idx]
                segment[position_idx] += 1
                if segment[position_idx] > max_bound[position_idx]:
                    segment[position_idx] = max_bound[position_idx]
                segment_sum = int(round(sum(segment)))

        for i in range(len(segment)):
            self.position[offset + i] = segment[i]

    def evaluate_fitness(self, fitness_func):
        self.fitness = fitness_func(self.position)

    def move(self, pheromone, alpha, beta):
        new_position = []
        for i in range(len(self.position)):
            probabilities = []
            min_bound, max_bound = self.bounds[i]
            for j in range(min_bound, max_bound + 1):
                # 각 위치에 대한 선택 확률 계산
                prob = (pheromone[i][j] ** alpha) * ((1.0 / (1 + abs(self.position[i] - j))) ** beta)
                probabilities.append(prob)
            probabilities = np.array(probabilities)
            probabilities /= probabilities.sum() # 확률의 합이 1이 되도록 정규화
            plus = np.random.choice(len(probabilities), p=probabilities)
            chosen_position = min_bound + plus # 확률에 따라 새로운 위치 선택
            chosen_position = min(max(chosen_position, min_bound), max_bound) # 위치가 경계를 벗어나지 않도록 조정
            new_position.append(chosen_position)
        self.position = new_position
        self.position = self.normalize_position(self.position) # 주기 통일


class ACO:
    def __init__(self, fitness_function, bounds, num_ants, max_iter, evaporation_rate, alpha, beta, interval_size, node_number):
        self.fitness_func = fitness_function
        self.bounds = bounds
        self.num_ants = num_ants
        self.max_iter = max_iter
        self.evaporation_rate = evaporation_rate
        self.alpha = alpha
        self.beta = beta
        self.node_number = node_number
        self.interval_size = interval_size
        self.pheromone = np.ones((len(bounds), max([b[1] for b in bounds])+1))
        #print('페로몬 초기:', self.pheromone)
        self.best_position = None
        self.best_fitness = float('inf')
        
    def run_result(self):
        for iteration in range(self.max_iter):
            # 각 iteration마다 새로운 ant 객체 생성
            self.ants = [Ant(self.bounds, self.interval_size, self.node_number) for _ in range(self.num_ants)]
            # 각 ant의 fitness 평가하기
            for ant in self.ants:
                ant.move(self.pheromone, self.alpha, self.beta)
                ant.evaluate_fitness(self.fitness_func)
                # global_best_position, global_best_fitness 업데이트
                if ant.fitness < self.best_fitness or self.best_fitness == -1:
                    self.best_position = list(ant.position)
                    self.best_fitness = float(ant.fitness)
            # 개미를 새로운 위치로 이동
            for ant in self.ants:
                ant.move(self.pheromone, self.alpha, self.beta)
            # 페로몬 업데이트
            self.update_pheromone(self.ants)
        # 각 iteration 결과 출력
        print('Best position:', self.best_position)
        print('Best fitness:', self.best_fitness)
        return self.best_position, self.best_fitness

    def update_pheromone(self, ants):
        print('페로몬 증발 전', self.pheromone)
        self.pheromone *= self.evaporation_rate # 페로몬 증발
        print('페로몬 증발 후', self.pheromone)
        Q = 1 # 페로몬 증가 상수
        for ant in ants:
            for i in range(len(ant.position)):
                self.pheromone[i][int(ant.position[i])] += Q / ant.fitness # 각 개미의 경로에 따라 페로몬 강화
            print('페로몬 강화', self.pheromone)

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
    return z

min_dur = [25, 12, 22, 28, 42, 25, 12, 15, 30, 51, 56, 19, 13, 1, 45]
cur_dur = [31, 17, 27, 38, 52, 33, 17, 22, 32, 61, 66, 22, 18, 4, 55]
max_dur = [41, 22, 32, 48, 62, 43, 22, 27, 42, 65, 76, 29, 23, 8, 65]

if __name__ == "__main__":
    bounds = []
    interval_size = []
    yellow_time = 3
    for i in range(len(min_dur)):
        bounds.append((min_dur[i], max_dur[i]))
        interval_size.append((max_dur[i] - min_dur[i])/yellow_time)
    num_ants = 2
    num_iterations = 3
    node_number = 15
    evaporation_rate = 0.8
    alpha = 1.0
    beta = 2.0
    
    start_time = time.time()  # 시작 시간 기록
    aco = ACO(objective_function, bounds, num_ants, num_iterations, evaporation_rate, alpha, beta, interval_size, node_number)
    best_position, best_fitness = aco.run_result()
    end_time = time.time()  # 종료 시간 기록

    elapsed_time = end_time - start_time
    print(f"Execution time: {elapsed_time} seconds")
    print("Best Position:", best_position)
    print("Best Fitness:", best_fitness)