# Import required libraries
import socket

# Define the server parameters
SERVER_HOST = 'localhost'
SERVER_PORT = 1234

# Define the server logic
def run_server():
    # Create server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))

    # Listen for incoming connections
    server_socket.listen()

    # Accept incoming connections
    client_socket, client_address = server_socket.accept()

    # Receive data from the client
    data = client_socket.recv(1024)

    # Process the data
    processed_data = data.upper()

    # Send a response back to the client
    client_socket.send(processed_data)

    # Close the connection
    client_socket.close()
    server_socket.close()

# Define the client parameters
CLIENT_HOST = 'localhost'
CLIENT_PORT = 1234
MESSAGE = 'Hello, World!'

# Define the client logic
def run_client():
    # Create client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect((CLIENT_HOST, CLIENT_PORT))

    # Send data to the server
    client_socket.send(MESSAGE.encode())

    # Receive response from the server
    response = client_socket.recv(1024)

    # Process the response
    processed_response = response.decode()

    # Print the processed response
    print(processed_response)

    # Close the connection
    client_socket.close()

# Run the server and client
if __name__ == '__main__':
    run_server()
    run_client()