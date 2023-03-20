import gym
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam


class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = []
        self.gamma = 0.95 # Discount factor
        self.epsilon = 1.0 # Exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()
        self.target_model = self._build_model()

    def _build_model(self):  
        input_state = Input(shape=(self.state_size,))
        x = Dense(24, activation='relu')(input_state)
        x = Dense(24, activation='relu')(x)
        x = Dense(self.action_size, activation='linear')(x)
        model = Model(inputs=input_state, outputs=x)
        model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return np.random.choice(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])

    def replay(self, batch_size):
        if len(self.memory) < batch_size:
            return
        minibatch = np.random.choice(self.memory, batch_size, replace=False)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                Q_next = np.amax(self.target_model.predict(next_state)[0])
                target = reward + self.gamma * Q_next
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

# Sumo 환경 설정 및 초기화
env = gym.make('Sumo-v0')
observation = env.reset()

# DQN Agent 설정 및 초기화
state_size = observation.shape[0]
action_size = env.action_space.n
agent = DQNAgent(state_size, action_size)

# 총 보상(total reward) 값을 저장할 리스트 생성
total_rewards = []

for episode in range(100):
    observation = env.reset()
    done = False
    total_reward = 0
    while not done:
        # DQN Agent에게 현재 상태 정보(state)를 전달하여 행동(action)을 결정하도록 함
        action = agent.act(observation.reshape(1, -1))

        # Sumo 환경에서 행동(action)을 수행하고, 보상(reward)과 다음 상태 정보(next state)를 얻음
        next_observation, reward, done, _ = env.step(action)

        # DQN Agent에서 (state, action, reward, next state) 샘플을 기억하고 모델을 업데이트함
        agent.remember(observation, action, reward, next_observation, done)
        agent.replay(batch_size=32)

        # 다음 상태 정보(next state)를 현재 상태 정보(state)로 업데이트함
        observation = next_observation
        
        # 총 보상(total reward) 값 계산
        total_reward += reward

    # 에피소드(episode)마다 총 보상(total reward) 값을 기록
    total_rewards.append(total_reward)

    # 결과 출력
    print("Episode: {}, Total Reward: {}".format(episode+1, total_reward))

# 총 보상(total reward) 값 그래프 출력
plt.plot(total_rewards)
plt.xlabel('Episode')
plt.ylabel('Total Reward')
plt.title('DQN Performance')
plt.show()

########################## 
####  종료 조건 추가  ####
