import socket
from _thread import *
import threading
import sys
import config

class Server:
    def __init__(self):

        self.host = ''
        self.port_number = 13000
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_buffer = 5
        self.authenticated_clients = []
        
    def authenticate(self, client_socket):

        connection_message = 'Enter password'
        client_socket.send(connection_message.encode('utf-8'))
        client_reply = client_socket.recv(len(config.PASSWORD) + 10)

        if client_reply.decode('utf-8') == config.PASSWORD:
            client_socket.send('Authenticated. Welcome!'.encode('utf-8'))    
            return 1
        else:
            client_socket.send('Incorrect password! Disconnecting'.encode('utf-8'))
            return 0 

    def getFiles(self):
        pass

    def sendFile(self):
        pass

    def run(self):
        

        self.server_socket.bind((self.host, self.port_number))
        # Listen for clients
        self.server_socket.listen(self.client_buffer)
        
        run_server = True
        
        while run_server:

            # Accepting connection with client
            client_socket, client_ip  = self.server_socket.accept()
            
            if client_socket not in self.authenticated_clients:
                auth = self.authenticate(client_socket)
                if auth == 0:
                    client_socket.close()
                else:
                    self.authenticated_clients.append(client_socket)
            else:
                print(client_socket, str(client_ip))

                
                command = client_socket.recv(1024)
                
                if command == 'quit':
                    client_socket.close()

if __name__ == "__main__":
    
    server = Server()
    server.run()