
# Importing necessary modules for socket communication, file operations, and system-specific parameters and functions
import socket  
import os  
import sys  

# Defining the buffer size for data transfer
BUFFER_SIZE = 1024  

# Main function to handle command-line arguments and socket connection
def main():  
    # Checking if the number of command-line arguments is not equal to 4
    if len(sys.argv) != 4:  
        # Displaying usage instructions
        print("Usage: python client.py <command> <filename> <port>")  
        return  # Exiting the program if usage is incorrect

    # Storing the command, filename, and port number from command-line arguments
    command = sys.argv[1]  
    filename = sys.argv[2]  
    port = int(sys.argv[3])  

    try:  # Exception handling for socket connection
        # Creating a TCP socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        # Connecting to the server
        client_socket.connect(('localhost', port))  

        # Sending command and filename to the server
        client_socket.sendall(f"{command} {filename}".encode())  

        # If command is 'get', receive file from server
        if command == 'get':  
            receive_file(client_socket, filename)
        # If command is 'upload', send file to server
        elif command == 'upload':  
            send_file(client_socket, filename)

    # Handling exceptions
    except Exception as e:  
        # Printing error message
        print(f"Error: {e}")  

    finally:  # Cleanup - closing the socket connection
        # Closing the client socket
        client_socket.close()  

# Function to send file to the server
def send_file(client_socket, filename):  
    try:  # Exception handling for file operations
        # Opening the file in binary mode
        with open(filename, 'rb') as file:  
            # Looping to read file in chunks and send to server
            while True:  
                # Reading a chunk of data from the file
                chunk = file.read(BUFFER_SIZE)  
                # Checking if end of file is reached
                if not chunk:  
                    break  # Exiting the loop if end of file is reached
                # Sending the chunk of data to the server
                client_socket.sendall(chunk)  
        # Printing success message after file is sent
        print(f"Sent {filename} to server")  

    # Handling file not found error
    except FileNotFoundError:  
        # Printing file not found error message
        print(f"File {filename} not found")  
        # Sending error message to the server
        client_socket.sendall(b"File not found")  

# Function to receive file from the server
def receive_file(client_socket, filename):  
    try:  # Exception handling for file operations
        # Creating a new file to write received data
        with open(f"new_{filename}", 'wb') as file:  
            # Looping to receive data in chunks from the server
            while True:  
                # Receiving a chunk of data from the server
                chunk = client_socket.recv(BUFFER_SIZE)  
                # Checking if end of file is reached
                if not chunk:  
                    break  # Exiting the loop if end of file is reached
                # Writing the received data to the file
                file.write(chunk)  
        # Printing success message after file is received
        print(f"Received {filename} from server")  

    # Handling exceptions
    except Exception as e:  
        # Printing error message if an exception occurs
        print(f"Error receiving file: {e}")  

# Check if the script is executed as main program
if __name__ == "__main__":  
    # Calling the main function if the script is executed directly
    main()  


