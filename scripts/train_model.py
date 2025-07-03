from client import Platform, read_or_create_q_table, binary_to_position_id, select_action, update_q_value, save_q_table
import connection
import numpy as np

# ================================
# Q-Learning parameters
# ================================
LEARNING_RATE = 0.1       # Learning rate (alpha) -> MODEL CONVERGENCE # NÃO AUMENTAR
DISCOUNT_FACTOR = 0.95     # Discount factor (gamma) -> RELATIVE TO PROBLEM
EPSILON = 0               # Exploration rate (epsilon) -> TRAINING MUTÁVEL

# ================================
# Action and Direction mappings
# ================================
ACTIONS = ['left', 'right', 'jump']
DIRECTION = ['N', 'E', 'S', 'W']

# ================================
# MAIN EXECUTION
# ================================

# Make sure the game server is running (/executables)
socket = connection.connect(2037)
if socket == 0:
    exit()

# Load or initialize Q-table
q_table = read_or_create_q_table()

# Number of training actions
num_actions = 1000000

# Initialize environment state
state_str, reward = connection.get_state_reward(socket, "none")
state_index = binary_to_position_id(state_str)
current_state = Platform(state_index, reward)

total_reward = 0
action_count = 0
# Training loop
for action in range(num_actions):
    # LEARNING_RATE = max(0.1, LEARNING_RATE - 0.00005)
    # EPSILON = LEARNING_RATE
    
    state_index, reward = current_state.get()
    total_reward += reward
    
    # Choose an action
    selected_action = select_action(q_table, state_index, EPSILON, ACTIONS)
    selected_action_index = ACTIONS.index(selected_action)

    # Execute action and get next state and reward
    new_state_str, reward = connection.get_state_reward(socket, selected_action)
    new_state_index = binary_to_position_id(new_state_str)

    # print('state_index:', state_index)
    # print('selected_action', selected_action)
    # print('reward:', reward)
    # print('new_state_index:', new_state_index)

    action_count += 1

    # Update Q-table
    update_q_value(q_table, state_index, reward, new_state_index, selected_action_index, LEARNING_RATE, DISCOUNT_FACTOR)
    
    if (action_count+1)% 100 == 0:
        avg_reward = total_reward / action_count
        total_reward = 0
        action_count = 0
        # print(f"Learning Rate: {LEARNING_RATE:.2f}")
        # print(f"Epsilon: {EPSILON:.2f}")
        print(f"Average Reward: {avg_reward:.2f}")
        # Save Q-table to file
    
    save_q_table(q_table, "data/new_q_table.txt")
    
    # Update internal state
    current_state.update(new_state_index, reward)

# def find_optimal_value_to_gamma():
#     num_actions = 1000
#     for gamma in [0.8, 0.85, 0.9, 0.95, 0.99]:
#         LEARNING_RATE = 1       # Learning rate (alpha)
#         EPSILON = 1    
#         q_table = np.zeros((24 * 4, 3), dtype=float)
#         total_reward = 0
#         for action in range(num_actions):
#             LEARNING_RATE = max(0.1, LEARNING_RATE - 0.0005)
#             EPSILON = LEARNING_RATE
            
#             state_index, reward = current_state.get()
#             total_reward += reward
            
#             # Choose an action
#             selected_action = select_action(q_table, state_index, EPSILON, ACTIONS)
#             selected_action_index = ACTIONS.index(selected_action)

#             # Execute action and get next state and reward
#             new_state_str, reward = connection.get_state_reward(socket, selected_action)
#             new_state_index = binary_to_position_id(new_state_str)

#             # Update Q-table
#             update_q_value(q_table, state_index, reward, new_state_index, selected_action_index, LEARNING_RATE, gamma)
            
#             avg_reward = total_reward / num_actions
#             # print(f"Learning Rate: {LEARNING_RATE:.2f}")
#             # print(f"Epsilon: {EPSILON:.2f}")
            
#             # Update internal state
#             current_state.update(new_state_index, reward)

#         print(f"Average Reward for gamma {gamma}: {avg_reward}")

# find_optimal_value_to_gamma()