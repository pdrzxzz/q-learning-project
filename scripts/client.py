import connection
import numpy as np
import random as rd

# Q-Learning parameters
LEARNING_RATE = 0.1
DISCOUNT_FACTOR = 0.99
EPSILON = 0.8

# Action mapping
ACTIONS = ['left', 'right', 'jump']


# Load the Q-table
q_table = np.loadtxt('data/q_table.txt', delimiter=',')
np.set_printoptions(precision=6)

# Initialize state and reward
state_index = 0
reward = -14

# Converts a 7-bit binary state string to an integer index for the Q-table
# State format: DDPPPPP (7 bits)
# - DD: Direction bits
#       00 = North
#       01 = East
#       10 = South
#       11 = West
# - PPPPP: Platform ID (0 to 23, in binary)
def binary_to_position_id(binary_state):
    return int(binary_state, 2)
# select_action function selects an action based on epsilon-greedy strategy
# If a random number is less than epsilon, it chooses a random action
# Otherwise, it selects the action with the highest Q-value for the current state
# action_list is a list of possible actions, and state_index is the index of the current
# state in the Q-table
# Returns the chosen action

def select_action(epsilon, action_list, state_index):
    if rd.random() < epsilon:
        chosen_action = action_list[rd.randint(0, len(action_list) - 1)]
        print(f"Random action chosen for state {state_index}: {chosen_action}")
    else:
        best_action_index = np.argmax(q_table[state_index])
        chosen_action = action_list[best_action_index]
        print(f"Best action chosen for state {state_index}: {chosen_action}")
    return chosen_action

# The Bellman equation is used to update the Q-value for a given state-action pair
# It calculates the target Q-value based on the immediate reward and the maximum Q-value
# of the next state, discounted by the discount factor gamma
# r is the immediate reward, s_prime is the next state index, and gamma is the discount factor
# Returns the target Q-value

def bellman_equation(r, s_prime, gamma):
    max_q = np.max(q_table[s_prime])
    q_target = r + gamma * max_q
    return q_target





# Before running this, ensure to be running the game first (/windows_exec, /linux_exec, /max_exec).

# Connect to game
socket = connection.connect(2037)
if socket == 0: # If fail to connect
    exit() # Stop execution

# Read data/q_table.txt

# Read actual state
state, reward = connection.get_state_reward(socket, "none")

# Take best action based on q_table
    # Retrieves best action based on state

    # Do the action
state, reward = connection.get_state_reward(socket, "best_action")

# Updates q_table based on reward

# Write q_table.txt