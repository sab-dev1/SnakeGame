import random
import numpy as np 
class Agent1 :
  def __init__(self, state_size , action_size  ) :
    self.action_size = action_size
    self.state_size = state_size 
    self.q_table = np.zeros((state_size[0], state_size[1],action_size))  #we initialize our Q-value table with a zero for each pair of state and action
    self.learning_rate = 0.1
    self.discount_factor = 0.9
    self.epsilon = 0.1
  def get_action(self, state) :
    if random.uniform(0 , 1) < self.epsilon: #we test if a random value chosen between 0 and 1 is lesser than our epsilon , this determines if the agent is going to explore or to exploit 
      return random.randint(0, self.q_table.shape[2] - 1)  #if so , the agent is going to explore (a random action is chosen from the range of possible actions)
    else:
      return np.argmax(self.q_table[state[0], state[1]])  #if not (exploitation) , this line selects the action with the highest Q-value for the given state using np.argmax
  def update_Q_table(self , current_state , action , reward , next_state ):
    current_q_value = self.q_table[current_state[0], current_state[1], action]
    max_next_q_value = np.max(self.q_table[next_state[0], next_state[1]])
    new_q_value = current_q_value + self.learning_rate * (reward + self.discount_factor * max_next_q_value - current_q_value)
    self.q_table[current_state[0], current_state[1], action] = new_q_value
  def get_reward(self, current_state, action, next_state):
    if next_state[0] < 0 or next_state[0] >= 70 or next_state[1] < 0 or next_state[1] >= 70 :
      return -10
    elif next_state[0] == self.apple_position_x // 10 and next_state[1] == self.apple_position_y // 10 :
      return 10
    else:
      return -1
    
   