import connection

socket = connection.connect(2037)
state, reward = connection.get_state_reward(socket, "vof")
print(state, reward)

