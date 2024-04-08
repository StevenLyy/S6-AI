import random
import gym
import math
import numpy as np
from pprint import pprint

env = gym.make("CartPole-v1")
alpha = 0.1  # learning rate [0...1]
gamma = 0.6  # discount factor [0...1]
epsilon = 1  # exploration variable
epsilon_decay = 0.995 # decay for exploration variable

q_table = np.zeros([env.observation_space.high.size, env.action_space.n])
state_space_size = env.observation_space
num_bins = [20, 20, 20, 20]


def discretize_state(state):
    discrete_state = (np.digitize(state, bins=np.linspace(env.observation_space.low, env.observation_space.high, num_bins + 1)[1:]) - np.ones(len(state)) ).astype(int)
    return discrete_state


def get_action(state):
    if random.uniform(0, 1) < epsilon:
        return env.action_space.sample()
    else:
        state_index = discretize_state(state)
        return np.argmax(q_table(state_index))

def update_q_table(state, action, reward, next_state):
    q_table[state][action] = (1-alpha) * q_table[state][action] + alpha * (reward + epsilon * np.max(q_table[next_state]))

episodes = 100
for _ in range(1, episodes + 1):
    state = env.reset()  # current state
    done = False
    score = 0

    while not done:
        env.render()
        action = get_action(state)
        next_state, reward, done, info = env.step(action)
        score += reward
        update_q_table(state, action, reward, next_state)
        epsilon *= epsilon_decay
        state = next_state
    print(f"episode: {_} ")
env.close()
