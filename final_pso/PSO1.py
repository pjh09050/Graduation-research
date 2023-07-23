import random
import numpy as np
from math import *
import matplotlib
import sys
matplotlib.rcParams['animation.embed_limit'] = 50.0 # 용량 제한 

class Particle:
    def __init__(self, bounds, max_iter, initial_position=None):
        self.position = []
        self.velocity = []
        self.best_position = []
        self.fitness = sys.maxsize
        self.best_fitness = sys.maxsize
        self.iteration = 0
        self.max_iter = max_iter
        if initial_position is not None:
            if len(initial_position) != len(bounds):
                raise ValueError("The length of initial_position must match the number of dimensions in the bounds.")
            self.position = list(initial_position)
        else:
            for i in range(len(bounds)):
                self.position.append(random.randint(bounds[i][0], bounds[i][1]))
        self.velocity = [random.uniform(-1, 1) for _ in range(len(bounds))]

    def evaluate_fitness(self, fitness_func):
        # current position에 대한 fitness 계산
        self.fitness = fitness_func(self.position)
        # best_position과 best_fitness 업데이트
        if self.fitness <= self.best_fitness:
            self.best_position = self.position
            self.best_fitness = self.fitness

    def update_velocity(self, global_best_position):
        print(global_best_position)
        print(self.best_position)
        w_min = 0.5
        w_max = 1
        self.iteration += 1
        w = w_max - ((w_max - w_min) * self.iteration / self.max_iter) # w가 점점 감소
        c1 = 1  # 자신의 최고 위치에 대한 가중치
        c2 = 2  # 집단의 최고 위치에 대한 가중치
        for i in range(len(self.position)):
            r1 = random.random() # 0,1 사이의 난수
            r2 = random.random()
            cognitive_velocity = c1 * r1 * (self.best_position[i] - self.position[i])
            social_velocity = c2 * r2 * (global_best_position[i] - self.position[i])
            self.velocity[i] = w * self.velocity[i] + cognitive_velocity + social_velocity

    def update_position(self, bounds):
        for i in range(len(self.position)):
            self.position[i] = self.position[i] + self.velocity[i]
            # adjust maximum position 
            if self.position[i] < bounds[i][0]:
                self.position[i] = bounds[i][0]
            # adjust minimum position 
            elif self.position[i] > bounds[i][1]:
                self.position[i] = bounds[i][1]

class PSO:
    def __init__(self, fitness_function, bounds, num_particles, max_iter, initial_positions=None):
        self.fitness_func = fitness_function
        self.bounds = bounds
        self.num_particles = num_particles
        self.max_iter = max_iter
        self.global_best_position = []
        self.global_best_fitness = -1  
        self.swarm = []
        if initial_positions:
            num_specified_positions = len(initial_positions)
            for i in range(num_specified_positions):
                self.swarm.append(Particle(bounds, self.max_iter, initial_position=initial_positions[i]))
            for i in range(num_particles - num_specified_positions):
                self.swarm.append(Particle(bounds, self.max_iter))
        else:
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
                    self.global_best_fitness = self.swarm[j].fitness
            # 각 particle의 position과 velocity 업데이트
            for j in range(self.num_particles):
                self.swarm[j].update_velocity(self.global_best_position)
                self.swarm[j].update_position(self.bounds)
        print('Best position:', self.global_best_position)
        print('Best fitness:', self.global_best_fitness)
        return self.global_best_position, self.global_best_fitness


