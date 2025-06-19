import connection

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