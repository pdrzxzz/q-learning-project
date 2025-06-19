import connection

socket = connection.connect(2037)
state, reward = connection.get_state_reward(socket, "front")
state, reward = connection.get_state_reward(socket, "jump")
state, reward = connection.get_state_reward(socket, "dowoo")
