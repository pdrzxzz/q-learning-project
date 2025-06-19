import socket  # Import the socket module to enable TCP/IP networking

# Creates a TCP connection
def connect(port):
    try:
        # Create a TCP socket using IPv4 addressing
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Attempt to connect to the server running on localhost (127.0.0.1) at the specified port
        s.connect(('127.0.0.1', port))  
        print('TCP connection established')  # Success message
        return s  # Return the connected socket object
    except:
        # If any exception occurs (e.g., connection refused, port closed), handle gracefully
        print('Failed to establish TCP connection as client')  
        return 0  # Return 0 to indicate failure
        # self.terminate()  # Placeholder for possible cleanup logic (not used here)

# Returns the state and reward that the agent received
def get_state_reward(s, action):
    # Action: "jump", "left" or "right"
    
    # Only send action to the server if it's valid
    if(action in ["jump", "left", "right"]):  # Only if valid action
        s.send(str(action).encode())  # Send the action (as string) to the server encoded as bytes
    
    print("action:", action)  # Print the action sent/requested
    
    data = ""  # Variable to hold the received raw data as a string
    data_recv = False  # Flag to indicate whether valid data has been received

    # Loop until a valid response is received and parsed
    while(not data_recv):
        # Receive up to 1024 bytes from the server and decode from bytes to string
        data = s.recv(1024).decode()  

        try:
            # Try to evaluate the received string into a Python dictionary
            # Expected format: "{'estado': '01', 'recompensa': -3}"
            data = eval(data)  
            data_recv = True  # If successful, mark data as received
        except:
            # If eval fails (e.g., due to malformed data), stay in the loop and try again
            data_recv = False  

    # Convert the received data to variables
    state = data['estado']       # 'estado' means state, e.g., "00" = North, "01" = East, etc.
    reward = data['recompensa']  # 'recompensa' means reward, a negative integer between -14 and -1

    print("state:", state)  # Print the current state
    print("reward:", reward)  # Print the received reward

    return state, reward  # Return the state and reward as a tuple
