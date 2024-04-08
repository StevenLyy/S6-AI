import random
import gym
import numpy as np
import matplotlib as plt
from gym.envs.toy_text.frozen_lake import generate_random_map

env = gym.make("FrozenLake-v1", render_mode='human', desc=generate_random_map(size=4))

action_space_count = env.action_space.n
state_space_count = env.observation_space.n

reward_win = 10
reward_step = 0
reward_falling = -20

episodes = 1000
alpha = 0.1  # learning rate
gamma = 0.99  # discount factor
epsilon = 1.0 # exploration rate
epsilon_decay = 0.99
q_table = np.zeros((state_space_count, action_space_count))
#q_table = np.random.uniform(low=0.8, high=1, size=(state_space_count, action_space_count))


def make_action(local_state):
    if random.uniform(0, 1) < epsilon:
        print('> exploring')
        return np.random.randint(0, action_space_count)
    else:
        return np.argmax(q_table[local_state])


def update_q_table(local_state, local_action, local_reward, local_next_state):
    max_q_next = np.max(q_table[local_next_state])  # Find the max Q-value of the next state
    q_table[local_state][local_action] = (1 - alpha) * q_table[local_state][local_action] + alpha * (local_reward + gamma * np.max(max_q_next))

def get_coordinates_from_state(state):


def get_distance_to_goal(state, goal_state):
  """
  Calculates the Manhattan distance between a state and the goal state.

  Args:
      state: The current state of the agent (integer representing the grid location).
      goal_state: The integer representing the location of the goal.

  Returns:
      The Manhattan distance between the state and the goal.
  """
  # Assuming goal_state is known (modify based on your environment)
  goal_x, goal_y = get_coordinates_from_state(goal_state)  # Function to extract coordinates from state
  current_x, current_y = get_coordinates_from_state(state)
  return abs(goal_x - current_x) + abs(goal_y - current_y)


for _ in range(episodes + 1):
    print(f"episode: {_}")
    state = env.reset()
    done = False
    episode_reward = 0

    while not done:
        action = make_action(state)
        next_state, reward, terminated, info = env.step(action)

        # Update reward based on environment feedback
        if reward == 0:
            reward = reward_step
        elif terminated and reward != reward_win:
            reward = reward_falling  # Penalty for falling into a hole
        elif terminated and reward == reward_win:
            reward = reward_win  # Reward for reaching the goal

        print(reward)
        update_q_table(state, action, reward, next_state)
        epsilon *= epsilon_decay
        episode_reward += reward
        state = next_state
        if terminated:
            env.reset()
            done = True
    print()
    print('===========================================')
    print('Q-table after training:')
    print(q_table)
    print(q_table.shape)

