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

def normalize_position(position):
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
    position = x1_adjusted + x2_adjusted + x3_adjusted
    return adjust_position(position)

def adjust_position(position):
    while True:
        x1_sum = int(round(sum(position[:5])))
        x2_sum = int(round(sum(position[5:10])))
        x3_sum = int(round(sum(position[10:])))
        if x1_sum == 165 and x2_sum == 165 and x3_sum == 165:
            break
        if x1_sum != 165:
            position[:5] = correct_segment(position[:5], 0, 165)
        if x2_sum != 165:
            position[5:10] = correct_segment(position[5:10], 5, 165)
        if x3_sum != 165:
            position[10:] = correct_segment(position[10:], 10, 165)
    return position

def correct_segment(segment, offset, target_sum):
    bounds = bounds_list[offset:offset + len(segment)]
    min_bound = [b[0] for b in bounds]
    max_bound = [b[1] for b in bounds]
    segment_sum = int(round(sum(segment)))

    if segment_sum > target_sum:
        minus_list = [1, 0, 2, 3, 4]
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

    return segment

def evaluate_fitness(position):
    start_time = time.time()
    generate_routefile()
    y = [num for num in position[:12] for num in (num, 3)]
    y.extend(position[12:13])
    y += [num for num in position[13:] for num in (num, 3)]
    y.extend([3])
    x1 = np.array(y[:10])
    x2 = np.array(y[10:20])
    x3 = np.array(y[20:30])
    traci.start([checkBinary('sumo'), "-c", "new1.sumocfg", "--tripinfo-output", "tripinfo.xml", "--quit-on-end", "--start", "--no-warnings"])
    modify_phase(x1, x2, x3)
    fitness = run()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Execution time: {elapsed_time} seconds")
    return fitness

def decode_chromosome(chromosome, bounds, interval_size):
    position = []
    for i in range(len(bounds)):
        gene = chromosome[i*4:(i+1)*4]
        DV = int(gene, 2)
        g_min, g_max = bounds[i]
        d = (g_max - g_min) / interval_size[i]
        g = g_min + ((g_max - g_min) / (2**d - 1)) * DV
        position.append(g)
    return normalize_position(position)


def genetic_algorithm(bounds, population_size, mutation_rate, crossover_rate, generations):
    interval_size = [(b[1] - b[0]) / 3 for b in bounds]
    # 초기 인구 생성: 각 개체는 이진 문자열로 표현
    population = [''.join(random.choice('01') for _ in range(len(bounds) * 4)) for _ in range(population_size)]
    best_fitness = float('inf')
    best_position = None
    #print('population', population)
    for generation in range(generations):
        fitness_scores = []
        for chromosome in population:
            #print('chromosome', chromosome)
            # 이진 문자열을 연속형 변수로 해독하여 포지션 얻기
            position = decode_chromosome(chromosome, bounds, interval_size)
            # fitness 함수 평가 (제약 위반에 대한 패널티 포함)
            fitness = evaluate_fitness(position)
            fitness_scores.append((chromosome, fitness))

        fitness_scores.sort(key=lambda x: x[1])

        if fitness_scores[0][1] < best_fitness:
            best_fitness = fitness_scores[0][1]
            best_position = decode_chromosome(fitness_scores[0][0], bounds, interval_size)

        new_population = [fitness_scores[i][0] for i in range(population_size // 2)]

        while len(new_population) < population_size:
            parent1, parent2 = random.sample(population, 2)
            if random.random() < crossover_rate:
                crossover_point = random.randint(1, len(bounds) * 4 - 1)
                child = parent1[:crossover_point] + parent2[crossover_point:]
            else:
                child = parent1

            if random.random() < mutation_rate:
                mutation_index = random.randint(0, len(bounds) * 4 - 1)
                child = list(child)
                child[mutation_index] = '1' if child[mutation_index] == '0' else '0'
                child = ''.join(child)
            new_population.append(child)

        population = new_population
        #print('population 후', population)
        print(f"Generation {generation} Best fitness: {best_fitness}")

    return best_position, best_fitness, fitness_scores[0][0]

if __name__ == "__main__":
    bounds_list = []
    min_dur = [25, 12, 22, 28, 42, 25, 12, 15, 30, 51, 56, 19, 13, 1, 45]
    max_dur = [41, 22, 32, 48, 62, 43, 22, 27, 42, 65, 76, 29, 23, 8, 65]

    for i in range(len(min_dur)):
        bounds_list.append((min_dur[i], max_dur[i]))

    population_size = 2
    crossover_rate = 0.8
    mutation_rate = 0.1
    generations = 2

    start_time = time.time()
    best_position, best_fitness, best_chromosome = genetic_algorithm(bounds_list, population_size, mutation_rate, crossover_rate, generations)
    end_time = time.time()

    elapsed_time = end_time - start_time
    print(f"Execution time: {elapsed_time} seconds")
    print("Best Position:", best_position)
    print("Best Fitness:", best_fitness)
    print("Best chromosome:", best_chromosome)
    
