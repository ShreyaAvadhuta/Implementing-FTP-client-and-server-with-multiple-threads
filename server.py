
import socket  # Importing the socket module for network communication
import threading  # Importing the threading module for concurrent execution
import os  # Importing the os module for file operations
import sys  # Importing the sys module for system-specific parameters and functions

BUFFER_SIZE = 1024  # Defining the buffer size for data transfer

# Class definition for client threads
class ClientThread(threading.Thread):
    # Constructor method to initialize client thread
    def __init__(self, client_socket, client_address):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.client_address = client_address

    # Run method to handle client requests
    def run(self):
        print(f"Connected to {self.client_address}")
        try:
            while True:
                data = self.client_socket.recv(BUFFER_SIZE).decode()
                if not data:
                    break

                command, filename = data.split()
                if command == 'get':
                    self.send_file(filename)
                elif command == 'upload':
                    self.receive_file(filename)

        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.client_socket.close()

    # Method to send file to the client
    def send_file(self, filename):
        try:
            with open(filename, 'rb') as file:
                while True:
                    chunk = file.read(BUFFER_SIZE)
                    if not chunk:
                        break
                    self.client_socket.sendall(chunk)
            print(f"Sent {filename} to {self.client_address}")

        except FileNotFoundError:
            print(f"File {filename} not found")
            self.client_socket.sendall(b"File not found")

    # Method to receive file from the client
    def receive_file(self, filename):
        try:
            with open(f"new_{filename}", 'wb') as file:
                while True:
                    chunk = self.client_socket.recv(BUFFER_SIZE)
                    if not chunk:
                        break
                    file.write(chunk)
            print(f"Received {filename} from {self.client_address}")

        except Exception as e:
            print(f"Error receiving file: {e}")

# Main function to start the FTP server
def main():
    if len(sys.argv) != 2:
        print("Usage: python server.py <port>")
        return

    try:
        port = int(sys.argv[1])
    except ValueError:
        print("Invalid port number")
        return

    # Creating a TCP server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', port))  # Binding the server socket to localhost and port
    server_socket.listen(5)  # Listening for incoming connections with maximum backlog of 5
    print(f"FTP Server started on port {port}")

    while True:
        client_socket, client_address = server_socket.accept()  # Accepting client connection
        client_thread = ClientThread(client_socket, client_address)  # Creating a new client thread
        client_thread.start()  # Starting the client thread

# Entry point of the script
if __name__ == "__main__":
    main()  # Calling the main function to start the server


