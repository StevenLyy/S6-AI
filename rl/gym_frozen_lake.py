import pickle
import random
import gym
import numpy as np
from gym.envs.toy_text.frozen_lake import generate_random_map
from matplotlib import pyplot as plt


def run(episodes, render=True, is_training=True):
    env = gym.make("FrozenLake-v1", map_name="8x8", render_mode='human' if render else None)

    action_space_count = env.action_space.n
    state_space_count = env.observation_space.n

    alpha = 0.1  # learning rate
    gamma = 0.99  # discount factor
    epsilon = 1.0  # exploration rate
    epsilon_decay_rate = 0.0001  # epsilon decay rate. 1/0.0001 = 10,000

    reward_win = 50
    reward_step = -1
    reward_fall = -5

    if is_training:
        q_table = np.zeros((state_space_count, action_space_count))
    else:
        f = open('frozen_lake8x8.pkl', 'rb')
        q_table = pickle.load(f)
        f.close()

    rewards_per_episode = np.zeros(episodes)

    for episode in range(episodes + 1):
        state = env.reset()
        done = False

        while not done:
            if random.uniform(0, 1) < epsilon:
                action = np.random.randint(0, action_space_count)
            else:
                action = np.argmax(q_table[state, :])

            next_state, reward, terminated, info = env.step(action)

            if terminated and reward == 1:
                reward += reward_win  # Reward for reaching the goal
                rewards_per_episode[episode] = reward
            elif terminated and reward == 0:
                reward += reward_fall  # Penalty for falling into a hole
            else:
                reward += reward_step

            epsilon = max(epsilon - epsilon_decay_rate, 0)
            if epsilon == 0:
                alpha = 0.0001

            q_table[state][action] = (1 - alpha) * q_table[state][action] + alpha * (
                    reward + gamma * np.max(q_table[next_state, :]))

            state = next_state
            if terminated:
                env.reset()
                done = True

    sum_rewards = np.zeros(episodes)

    for t in range(episodes):
        sum_rewards[t] = np.sum(rewards_per_episode[max(0, t - 100):(t + 1)])
        plt.plot(sum_rewards)
        plt.savefig('frozen_lake8x8.png')

    if is_training:
        f = open("frozen_lake8x8.pkl", "wb")
        pickle.dump(q_table, f)
        f.close()


run(12000, render=False, is_training=True)
