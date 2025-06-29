import connection
import numpy as np
import random as rd
import time

# ================================
# Q-Learning parameters
# ================================
LEARNING_RATE = 0.1         # Learning rate (alpha)
DISCOUNT_FACTOR = 0.99      # Discount factor (gamma)
EPSILON = 0.2               # Exploration rate (epsilon)

# ================================
# Action and Direction mappings
# ================================
ACTIONS = ['left', 'right', 'jump']
DIRECTION = ['N', 'E', 'S', 'W']


class Platform:
    """
    Class to represent the current state and reward of the environment.
    """

    def __init__(self, initial_state, initial_reward):
        self.state = initial_state
        self.reward = initial_reward

    def update(self, new_state, new_reward):
        """
        Updates the current state and reward.
        """
        self.state = new_state
        self.reward = new_reward
        print(f"State: {self.state}, Reward: {self.reward}")

    def get(self):
        """
        Returns the current state and reward.
        """
        return self.state, self.reward


def read_or_create_q_table(new_file='data/new_q_table.txt',
                           initial_file='data/initial_q_table.txt',
                           default_value=1):
    """
    Tries to load the Q-table from `new_file`. 
    If that fails, tries to load from `initial_file`. 
    If ambos falham, cria uma Q-table zerada com a última coluna iniciada em default_value.

    Args:
        new_file (str): path to the newest Q-table.
        initial_file (str): path to the backup/initial Q-table.
        default_value (float): value to initialize the 'jump' column if creating from zero.

    Returns:
        np.ndarray: matriz da Q-table com shape (24*4, 3).
    """
    num_states     = 24
    num_directions = 4
    num_actions    = 3

    # 1) Try to load the most recent table
    try:
        q_table = np.loadtxt(new_file, delimiter=' ')
        np.set_printoptions(precision=6)
        print(f"Loaded Q-table from '{new_file}'.")
        return q_table
    except IOError:
        print(f"Could not load '{new_file}', trying '{initial_file}'...")

    # 2) Fallback: try to load the initial table
    try:
        q_table = np.loadtxt(initial_file, delimiter=' ')
        np.set_printoptions(precision=6)
        print(f"Loaded Q-table from '{initial_file}'.")
        return q_table
    except IOError:
        print(f"Could not load '{initial_file}'. Creating a new Q-table.")

    # 3) If ambos falharam, cria uma tabela nova
    q_table = np.zeros((num_states * num_directions, num_actions), dtype=float)
    q_table[:, -1] = default_value
    print("New Q-table created with default jump values.")
    return q_table



def save_q_table(q_table, filename):
    """
    Saves the Q-table to a file using NumPy's savetxt function.

    Args:
        q_table (np.ndarray): The Q-table matrix.
        filename (str): Path to the output file.
    """
    np.savetxt(filename, q_table, fmt='%.6f', delimiter=' ')
    print(f"Q-table successfully saved to '{filename}'!")


def binary_to_position_id(binary_state):
    """
    Converts a 7-bit binary state string to an integer index for the Q-table.

    Binary format: DDPPPPP
    - DD: Direction bits (00=N, 01=E, 10=S, 11=W)
    - PPPPP: Platform ID (0–23)

    Args:
        binary_state (str): State string, e.g., '0b0101101'

    Returns:
        int: Index in the Q-table
    """
    if binary_state.startswith("0b"):
        binary_state = binary_state[2:]

    direction = int(binary_state[:2], 2)
    platform_id = int(binary_state[2:], 2)
    return direction * 24 + platform_id


def select_action(state_index):
    """
    Selects an action using an epsilon-greedy strategy.

    Args:
        state_index (int): Current state index in Q-table.

    Returns:
        str: Selected action from ACTIONS.
    """
    if rd.random() < EPSILON:
        chosen_action = ACTIONS[rd.randint(0, len(ACTIONS) - 1)]
        print(f"Random action chosen: {chosen_action}")
    else:
        best_action_index = np.argmax(q_table[state_index])
        chosen_action = ACTIONS[best_action_index]
        print(f"Best action chosen {DIRECTION[state_index % 4]}: {chosen_action}")
    return chosen_action


def update_q_value(q_table, current_state_index, reward, next_state_index, selected_action_index):
    """
    Updates the Q-value for the current state-action pair using the Bellman equation.

    Q(s,a) = Q(s,a) + α * (r + γ * max(Q(s',a')) - Q(s,a))

    Args:
        q_table (np.ndarray): The Q-table.
        current_state_index (int): Index of current state.
        reward (float): Immediate reward.
        next_state_index (int): Index of next state.
        selected_action_index (int): Index of the action taken.
    """
    q_value = q_table[current_state_index, selected_action_index]
    print(f"Q-value for action {ACTIONS[selected_action_index]}: {q_value}")

    future_max_value = np.max(q_table[next_state_index])

    new_q_value = q_value + LEARNING_RATE * (reward + DISCOUNT_FACTOR * future_max_value - q_value)
    print(f"New Q-value for action {ACTIONS[selected_action_index]}: {new_q_value}")

    q_table[current_state_index, selected_action_index] = new_q_value


# ================================
# MAIN EXECUTION
# ================================

# Make sure the game server is running (windows_exec, linux_exec, etc.)
socket = connection.connect(2037)
if socket == 0:
    exit()

# Load or initialize Q-table
q_table = read_or_create_q_table()

# Number of training episodes
num_episodes = 100

# Initialize environment state
state_str, reward = connection.get_state_reward(socket, "none")
state_index = binary_to_position_id(state_str)
current_state = Platform(state_index, reward)

# Training loop
for episode in range(num_episodes):
    print(f"Episode: {episode}")
    
    state_index, reward = current_state.get()
    
    # Choose an action
    selected_action = select_action(state_index)
    selected_action_index = ACTIONS.index(selected_action)

    # Execute action and get next state and reward
    new_state_str, reward = connection.get_state_reward(socket, selected_action)
    new_state_index = binary_to_position_id(new_state_str)

    # Update Q-table
    update_q_value(q_table, state_index, reward, new_state_index, selected_action_index)

    # Save Q-table to file
    save_q_table(q_table, "data/new_q_table.txt")

    # Update internal state
    current_state.update(new_state_index, reward)

    time.sleep(0.1)
