from multiprocessing import Pool
import numpy as np
import random
from tqdm import tqdm

import random
from collections import defaultdict
import multiprocessing as mp
from itertools import product

class NimQAgent:
    def __init__(self, learning_rate=0.1, discount_factor=0.95, exploration_rate=1.0, exploration_decay=0.99):
        self.learning_rate = learning_rate  # Alpha
        self.discount_factor = discount_factor  # Gamma
        self.exploration_rate = exploration_rate  # Epsilon
        self.exploration_decay = exploration_decay  # Decay rate of epsilon per episode
        self.q_table = defaultdict(float)  # Initialize Q-table as a default dictionary
        
    def get_state_key(self, state):
        return str(state)
    
    def choose_action(self, state):
        if random.uniform(0, 1) < self.exploration_rate:
            available_piles = [i for i, coins in enumerate(state) if coins > 0]
            if not available_piles:
                return None
            pile = random.choice(available_piles)
            coins = random.randint(1, state[pile])
            return (pile, coins)
        else:
            best_action = None
            best_value = float('-inf')
            for pile, coins in enumerate(state):
                if coins > 0:
                    for coins_to_remove in range(1, coins + 1):
                        action = (pile, coins_to_remove)
                        q_value = self.q_table.get((self.get_state_key(state), action), 0)
                        if q_value > best_value:
                            best_value = q_value
                            best_action = action
            return best_action if best_action else None
        
    def update_q_table(self, state, action, reward, next_state):
        old_value = self.q_table[(self.get_state_key(state), action)]
        future_actions = [self.q_table[(self.get_state_key(next_state), (pile, coins))] 
                          for pile, coins in product(range(len(next_state)), range(1, max(next_state)+1)) 
                          if next_state[pile] >= coins]
        future_max = max(future_actions) if future_actions else 0
        new_value = old_value + self.learning_rate * (reward + self.discount_factor * future_max - old_value)
        self.q_table[(self.get_state_key(state), action)] = new_value
        
    def reduce_exploration(self):
        self.exploration_rate *= self.exploration_decay

    def train_single_episode(self, initial_state):
        state = list(initial_state)
        while sum(state) > 0:
            action = self.choose_action(state)
            if action is None:
                break
            pile, coins = action
            next_state = state[:]
            next_state[pile] -= coins
            reward = 1 if sum(next_state) == 0 else 0
            self.update_q_table(state, action, reward, next_state)
            state = next_state
        self.reduce_exploration()

    def train(self, initial_state, episodes=1000, pool_size=mp.cpu_count()):
        with Pool(pool_size) as p:
            p.map(self.train_single_episode_wrapper, tqdm([initial_state] * episodes))

    def train_single_episode_wrapper(self, initial_state):
        self.train_single_episode(initial_state)
    def predict(self, state):
        best_action = self.choose_action(state)
        return best_action


# Example usage
agent = NimQAgent()
initial_state = [3, 4, 5]
agent.train(initial_state, episodes=1000000)

# Test the trained model
state = (3, 4, 5)
action = agent.predict(state)
print(agent.q_table)
print(f"For state {state}, the best action is: Remove {action[1]} coins from pile {action[0]}")
