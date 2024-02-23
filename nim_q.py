import numpy as np
import random
from tqdm import tqdm

class NimQLearning:
    def __init__(self, stacks, alpha=0.5, gamma=0.9, epsilon=0.1):
        self.stacks = stacks  # List of integers representing the initial state
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration rate
        self.q_table = {}  # Use a dictionary for the Q-table, since state and action spaces can be large

    def get_possible_actions(self, state):
        actions = []
        for stack_index, coins in enumerate(state):
            for coins_to_remove in range(1, coins + 1):
                actions.append((stack_index, coins_to_remove))
        return actions

    def is_terminal_state(self, state):
        return all(coins == 0 for coins in state)

    def take_action(self, state, action):
        new_state = list(state)
        stack_index, coins_to_remove = action
        new_state[stack_index] -= coins_to_remove
        return tuple(new_state)

    def get_next_state_reward(self, state, action):
        # Check if the game ends after this action, i.e., all stacks are empty
        next_state = self.take_action(state, action)
        reward = 1 if self.is_terminal_state(next_state) else 0
        return next_state, reward

    def choose_action(self, state):
        if random.uniform(0, 1) < self.epsilon:
            # Exploration
            actions = self.get_possible_actions(state)
            action = random.choice(actions)
        else:
            # Exploitation
            actions = self.get_possible_actions(state)
            q_values = [self.q_table.get((state, action), 0) for action in actions]
            max_q_value = max(q_values)
            # In case there are multiple actions with the same Q-value
            max_actions = [actions[i] for i in range(len(actions)) if q_values[i] == max_q_value]
            action = random.choice(max_actions)
        return action

    def update_q_table(self, state, action, reward, next_state):
        old_value = self.q_table.get((state, action), 0)
        future_rewards = [self.q_table.get((next_state, a), 0) for a in self.get_possible_actions(next_state)]
        max_future_reward = max(future_rewards, default=0)  # Default to 0 if next state is terminal
        self.q_table[(state, action)] = old_value + self.alpha * (reward + self.gamma * max_future_reward - old_value)

    def play(self):
        state = tuple(self.stacks)
        while not self.is_terminal_state(state):
            action = self.choose_action(state)
            next_state, reward = self.get_next_state_reward(state, action)
            self.update_q_table(state, action, reward, next_state)
            state = next_state
    def get_best_action(self, state):
        """
        Returns the best action for a given state according to the Q-table.
        """
        state = tuple(state)  # Ensure the state is in tuple form
        if self.is_terminal_state(state):
            return None  # No action to be taken if the game is already over

        actions = self.get_possible_actions(state)
        q_values = [self.q_table.get((state, action), float('-inf')) for action in actions]
        max_q_value = max(q_values)
        # Find actions that have the maximum Q-value
        max_actions = [actions[i] for i, q_value in enumerate(q_values) if q_value == max_q_value]
        # Choose randomly among the best actions if there are multiple
        best_action = random.choice(max_actions)
        return best_action



# Example of training the model
if __name__ == "__main__":
    # Initialize the game with 3 stacks
    game = NimQLearning([3, 4, 5])
    
    # Train over 1000 episodes
    for episode in tqdm(range(1000000)):
        game.play()
    
    test_state = [3, 4, 5]
    best_action = game.get_best_action(test_state)
    print(f"Best action for state {test_state}: {best_action}")
    # Inspect the Q-table
    print("Q-table after training:")
    for key in game.q_table:
        print(f"State, Action: {key}, Q-value: {game.q_table[key]}")
