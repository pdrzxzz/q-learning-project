import socket

# Creates a TCP connection
def connect(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', port))  # Attempt to connect to localhost on the given port
        print('TCP connection established')
        return s
    except:
        print('Failed to establish TCP connection as client')
        return 0  # Return 0 if connection fails
        # self.terminate()  # Placeholder for possible cleanup logic

# Returns the state and reward that the agent received
def get_state_reward(s, action):
    # action: "jump", "left" or "right"
    if(action in ["jump", "left", "right"]): # Only if valid action
        s.send(str(action).encode())  # Send the actionion (as string) to the server  
    data = ""
    data_recv = False
    while(not data_recv):
        data = s.recv(1024).decode()  # Receive data from the server
        try:
            data = eval(data)  # Attempt to evaluate the string as a Python dictionary
            data_recv = True
        except:
            data_recv = False  # If eval fails, continue waiting for valid data

    # Convert the received data to variables
    state = data['estado']       # 'estado' means state
    reward = data['recompensa']  # 'recompensa' means reward

    return state, reward  # Return the state and reward

