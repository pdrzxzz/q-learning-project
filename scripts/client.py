import connection

# connect to game
socket = connection.connect(2037)

# read data/q_table.txt

# read actual state
state, reward = connection.get_state_reward(socket, "none")

# take best action based on q_table
    # retrieves best action based on state

    # do the action
state, reward = connection.get_state_reward(socket, "best_action")

# updates q_table based on reward

# write q_table.txt