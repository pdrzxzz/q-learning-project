import connection
import numpy as np
import random as rd

# Q-Learning parameters
LEARNING_RATE = 0.1
DISCOUNT_FACTOR = 0.99
EPSILON = 0.8

# Action mapping
ACTIONS = ['left', 'right', 'jump']

# Direction mapping
DIRECTION = ['N', 'E', 'S', 'W']

class Plataform:

    def __init__(self, estado_inicial, recompensa_inicial):
        self.state = estado_inicial
        self.reward = recompensa_inicial

    def update(self, novo_estado, nova_recompensa):
        self.state = novo_estado
        self.reward = nova_recompensa
        print(f"State: {self.state}, Reward: {self.reward}")

    def get(self):
        return self.state, self.reward
    
# Function to read or create a Q-table
def Read_or_Create_Q_Table(value=1, boolean=False):
    if(boolean):
        # If boolean is True, load the Q-table from a file
        try:
            q_table = np.loadtxt('data/q_table.txt', delimiter=',')
            np.set_printoptions(precision=6)
            print("Q-table loaded successfully.")
        except IOError:
            print("Failed to load Q-table from file.")
    else:
        # If boolean is False, create a new Q-table with the specified value
        numero_de_estados = 24
        numero_de_direcao = 4
        numero_de_valores = 3
        q_table = np.zeros((numero_de_estados * numero_de_direcao, numero_de_valores), dtype=float)
        q_table[:, -1] = value  # Set the jump column to the specified value
    return q_table

# Save q table to a file using NumPy's savetxt function
def save_q_table(q_table, nome_do_arquivo):
    # Salva o array no arquivo de texto
    # fmt='%.8f' formata cada número como um float com 8 casas decimais
    np.savetxt(nome_do_arquivo, q_table, fmt='%.6f', delimiter=' ')
    print(f"(Alternativa) Q-table salva com sucesso em '{nome_do_arquivo}'!")

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
def select_action(state_index):
    if rd.random() < EPSILON:
        chosen_action = ACTIONS[rd.randint(0, len(ACTIONS) - 1)]
        print(f"Random action chosen : {chosen_action}")
    else:
        best_action_index = np.argmax(q_table[state_index])
        chosen_action = ACTIONS[best_action_index]
        print(f"Best action chosen {DIRECTION[state_index%4]}: {chosen_action}")
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