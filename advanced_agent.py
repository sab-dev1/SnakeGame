import random
import numpy as np
from collections import deque

class Agent1:
    def __init__(self, state_size, action_size, batch_size=32, buffer_size=10000): # batch_size refers to the number of training examples used in one iteration of the optimization algorithm 
        self.action_size = action_size
        self.state_size = state_size
        self.q_table1 = np.zeros((state_size[0], state_size[1], action_size))
        self.q_table2 = np.zeros((state_size[0], state_size[1], action_size)) # we use two q-value tables as a technique to avoid the overestimation biais caused by the classical way of calculating the q-value based on the maximum q_values of the next states 
        self.learning_rate = 0.1
        self.discount_factor = 0.9
        self.epsilon = 0.1
        self.batch_size = batch_size
        self.buffer = deque(maxlen=buffer_size)   #we've also added a buffer to store all the past experiences , so that the agent can learn from them with a maximum lenght of buffer_size 

    def get_action(self, state):
        if random.uniform(0, 1) < self.epsilon:
            return random.randint(0, self.action_size - 1)
        else:
            return np.argmax(self.q_table1[state[0], state[1]] + self.q_table2[state[0], state[1]])

    def update_Q_table(self, current_state, action, reward, next_state):
        # Store experience in replay buffer
        self.buffer.append((current_state, action, reward, next_state)) # after each action we add the current_state , the action , the reward and the next state to the buffer

        # Sample mini-batch from replay buffer
        mini_batch = random.sample(self.buffer, self.batch_size) # we randomly sample a mini-batch from the the experiences in our buffer 

        for state, action, reward, next_state in mini_batch:
            # Calculate TD-error
            current_q_value1 = self.q_table1[state[0], state[1], action]
            current_q_value2 = self.q_table2[state[0], state[1], action]
            max_next_q_value1 = np.max(self.q_table1[next_state[0], next_state[1]])
            max_next_q_value2 = np.max(self.q_table2[next_state[0], next_state[1]])
            td_error1 = reward + self.discount_factor * max_next_q_value2 - current_q_value1
            td_error2 = reward + self.discount_factor * max_next_q_value1 - current_q_value2 # td error ( temporal difference errors ) represents the difference between the estimated value of a state-action pair and the actual reward plus the estimated value of the next state-action pair 

            # Update Q-values
            self.q_table1[state[0], state[1], action] += self.learning_rate * td_error1
            self.q_table2[state[0], state[1], action] += self.learning_rate * td_error2

    def get_reward(self, current_state, action, next_state):
        if next_state[0] < 0 or next_state[0] >= self.state_size[0] or next_state[1] < 0 or next_state[1] >= self.state_size[1]:
            return -10
        elif next_state[0] == self.apple_position_x // 10 and next_state[1] == self.apple_position_y // 10:
            return 10
        else:
            return -1
