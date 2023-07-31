import random
from math import *
import sys

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
            self.position.append(int(round(random.uniform(bounds[i][0], bounds[i][1]))))
            self.velocity.append(random.uniform(-1, 1))
        # x1_sum = sum(self.position[:5])
        # x2_sum = sum(self.position[5:10])
        # x3_sum = sum(self.position[10:])
        # print('초기해', self.position, x1_sum, x2_sum, x3_sum, sum(self.position))
        while True:
            x1_sum = int(round(sum(self.position[:5])))
            x2_sum = int(round(sum(self.position[5:10])))
            x3_sum = int(round(sum(self.position[10:])))
            if x1_sum == 165 and x2_sum == 165 and x3_sum == 165:
                break

            if x1_sum > 165:
                sort_list = sorted(self.position[:5], reverse=True)
                for i in range(len(sort_list)):
                    if int(round(sum(self.position[:5]))) == 165:
                        break
                    largest_value_idx = self.position.index(sort_list[i])
                    self.position[largest_value_idx] -= 1
                    self.position[largest_value_idx] = int(round(self.position[largest_value_idx]))
            else:
                sort_list = sorted(self.position[:5], reverse=False)
                for i in range(len(sort_list)):
                    if int(round(sum(self.position[:5]))) == 165:
                        break
                    smallest_value_idx = self.position.index(sort_list[i])
                    self.position[smallest_value_idx] += 1
                    self.position[smallest_value_idx] = int(round(self.position[smallest_value_idx]))

            if x2_sum > 165:
                sort_list = sorted(self.position[5:10], reverse=True)
                for i in range(len(sort_list)):
                    if int(round(sum(self.position[5:10]))) == 165:
                        break
                    largest_value_idx = self.position.index(sort_list[i], 5, 10)
                    self.position[largest_value_idx] -= 1
                    self.position[largest_value_idx] = int(round(self.position[largest_value_idx]))
            else:
                sort_list = sorted(self.position[5:10], reverse=False)
                for i in range(len(sort_list)):
                    if int(round(sum(self.position[5:10]))) == 165:
                        break
                    smallest_value_idx = self.position.index(sort_list[i], 5, 10)
                    self.position[smallest_value_idx] += 1
                    self.position[smallest_value_idx] = int(round(self.position[smallest_value_idx]))

            if x3_sum > 165:
                sort_list = sorted(self.position[10:], reverse=True)
                for i in range(len(sort_list)):
                    if int(round(sum(self.position[10:]))) == 165:
                        break
                    largest_value_idx = self.position.index(sort_list[i], 10)
                    self.position[largest_value_idx] -= 1
                    self.position[largest_value_idx] = int(round(self.position[largest_value_idx]))
            else:
                sort_list = sorted(self.position[10:], reverse=False)
                for i in range(len(sort_list)):
                    if int(round(sum(self.position[10:]))) == 165:
                        break
                    smallest_value_idx = self.position.index(sort_list[i], 10)
                    self.position[smallest_value_idx] += 1
                    self.position[smallest_value_idx] = int(round(self.position[smallest_value_idx]))

        # x1_sum = sum(self.position[:5])
        # x2_sum = sum(self.position[5:10])
        # x3_sum = sum(self.position[10:])
        # print('수정된 초기해', self.position, x1_sum, x2_sum, x3_sum, sum(self.position))

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

        # x1_sum = sum(self.position[:5])
        # x2_sum = sum(self.position[5:10])
        # x3_sum = sum(self.position[10:])
        # print('update 전 position', self.position, x1_sum, x2_sum, x3_sum, sum(self.position))
        while True:
            x1_sum = int(round(sum(self.position[:5])))
            x2_sum = int(round(sum(self.position[5:10])))
            x3_sum = int(round(sum(self.position[10:])))
            if x1_sum == 165 and x2_sum == 165 and x3_sum == 165:
                break

            if x1_sum > 165:
                sort_list = sorted(self.position[:5], reverse=True)
                for i in range(len(sort_list)):
                    if int(round(sum(self.position[:5]))) == 165:
                        break
                    largest_value_idx = self.position.index(sort_list[i])
                    self.position[largest_value_idx] -= 1
                    self.position[largest_value_idx] = int(round(self.position[largest_value_idx]))
            else:
                sort_list = sorted(self.position[:5], reverse=False)
                for i in range(len(sort_list)):
                    if int(round(sum(self.position[:5]))) == 165:
                        break
                    smallest_value_idx = self.position.index(sort_list[i])
                    self.position[smallest_value_idx] += 1
                    self.position[smallest_value_idx] = int(round(self.position[smallest_value_idx]))

            if x2_sum > 165:
                sort_list = sorted(self.position[5:10], reverse=True)
                for i in range(len(sort_list)):
                    if int(round(sum(self.position[5:10]))) == 165:
                        break
                    largest_value_idx = self.position.index(sort_list[i], 5, 10)
                    self.position[largest_value_idx] -= 1
                    self.position[largest_value_idx] = int(round(self.position[largest_value_idx]))
            else:
                sort_list = sorted(self.position[5:10], reverse=False)
                for i in range(len(sort_list)):
                    if int(round(sum(self.position[5:10]))) == 165:
                        break
                    smallest_value_idx = self.position.index(sort_list[i], 5, 10)
                    self.position[smallest_value_idx] += 1
                    self.position[smallest_value_idx] = int(round(self.position[smallest_value_idx]))

            if x3_sum > 165:
                sort_list = sorted(self.position[10:], reverse=True)
                for i in range(len(sort_list)):
                    if int(round(sum(self.position[10:]))) == 165:
                        break
                    largest_value_idx = self.position.index(sort_list[i], 10)
                    self.position[largest_value_idx] -= 1
                    self.position[largest_value_idx] = int(round(self.position[largest_value_idx]))
            else:
                sort_list = sorted(self.position[10:], reverse=False)
                for i in range(len(sort_list)):
                    if int(round(sum(self.position[10:]))) == 165:
                        break
                    smallest_value_idx = self.position.index(sort_list[i], 10)
                    self.position[smallest_value_idx] += 1
                    self.position[smallest_value_idx] = int(round(self.position[smallest_value_idx]))

        x1_sum = sum(self.position[:5])
        x2_sum = sum(self.position[5:10])
        x3_sum = sum(self.position[10:])
        # print('update 후 position', self.position, x1_sum, x2_sum, x3_sum, sum(self.position))

class PSO:
    def __init__(self, fitness_function, bounds, num_particles, max_iter):
        self.fitness_func = fitness_function
        self.bounds = bounds
        self.num_particles = num_particles
        self.max_iter = max_iter
        self.global_best_position = []  # group best position
        self.global_best_fitness = -1  # group best fitness
        self.swarm = [] # 초기 particles
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
                    self.global_best_fitness = float(self.swarm[j].fitness)
            # 각 particle의 position과 velocity 업데이트
            for j in range(self.num_particles):
                self.swarm[j].update_velocity(self.global_best_position)
                self.swarm[j].update_position(self.bounds)
        print('Best position:', self.global_best_position)
        print('sum best position', sum(self.global_best_position))
        print('Best fitness:', self.global_best_fitness)
        return self.global_best_position, self.global_best_fitness


