import socket
from _thread import *
import threading
import sys
import config
import hashlib
import os
import time
'''
Authors:
Ajay Shrihari & Rahul Sajnani
'''

class Server:
    def __init__(self):

        self.host = ''
        self.port_number = 13000
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_buffer = 5
        self.authenticated_clients = []
        
    def authenticate(self, client_socket):
        '''
        Function to authenticate client
        Input:
            client_socket - client socket object
        Returns:
            1 - if client is authenticated
            0 - else
        '''
        connection_message = 'Enter password'
        client_socket.send(connection_message.encode('utf-8'))
        client_reply = client_socket.recv(len(config.PASSWORD) + 10)

        if client_reply.decode('utf-8') == config.PASSWORD:
            client_socket.send('1'.encode('utf-8'))    
            return 1
        else:
            client_socket.send('0'.encode('utf-8'))
            return 0 

    def getFiles(self, arg, start_time, end_time, files=''):
        '''
        '''
        pass

    def sendFile(self, client_socket, filename):
        '''
        Function to send files to client(client download file)
        Output : should contain the filename , filesize ,
        lastmodified timestamp and the MD5hash of the
        requested file.
        TODO:
            - Get the file
            - Send the file to client
        Input:
            client_socket - client socket object
            filename - filename to the respective file
        Returns:
            None 
        '''
        file = open(filename, 'rb')
        reading = file.read(1024)
        while (reading):
            client_socket.send(reading)
            reading = file.read(1024)
        file_stats = os.stat(filename)
        file_mtime = time.localtime(os.path.getmtime(filename))
        file_mtime = time.strftime('%Y-%m-%d %H:%M:%S',file_mtime) 
        file.close()
        hasher = hashlib.md5(open(filename,'rb').read()).hexdigest()
        print ("Sending...")
        print ("Filename:%s, Filesize(Bytes):%s,Timestamp:%s,MD5hash:%s"%(filename,str(file_stats.st_size),str(file_mtime), str(hasher)))
        
    
    def getFileHash(self, client_socket, arg, filename=''):
        '''
        Function to get file hash and send a response to the client
        check deocde_command for info of how this will be called.
        TODO:
            - Get the file hash
            - Send the response to client
            - Handle the case when the file does not exist
        Input:
            client_socket - client socket object
            filename - filename to the respective file
            arg - checkall | verify
        Returns:
            None
        '''
        

        pass

    def client_session(self, client_socket):
        '''
        Function to execute client commands.
        Input:
            client_socket - client socket object
        Returns:
            None
        '''

        client_loop = True
        while client_loop:

            command = client_socket.recv(1024)
            command = command.decode('utf-8')
            
            command_list = command.split(' ')
            print(command_list)

            if command_list[0] == 'FileHash':

                if command_list[1] == 'verify':
                    self.getFileHash(client_socket, command_list[1], command_list[2])
                    
                elif command_list[1] == 'checkall':
                    self.getFileHash(client_socket, command_list[1])


            elif command_list[0] == 'FileDownload':
                self.sendFile(client_socket, command_list[1])

                pass

            elif command_list[0] == 'IndexGet':

                if command_list[1] == 'shortlist':
                    self.getFiles(command_list[1], command_list[2], command_list[3], command_list[4])
                elif command_list[1] == 'longlist':
                    self.getFiles(command_list[1], command_list[2], command_list[3], command_list[4])
                
                pass
            
            elif command_list[0] == 'quit':
                client_loop = False
                print('client closed')
                client_socket.close()

                

    def run(self):
        '''
        Runs server
        Input: 
            None
        Returns:
            None
        
        '''

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
                    print(str(client_ip))
                    self.client_session(client_socket)
                
                        
                        

                        

if __name__ == "__main__":
    
    server = Server()
    server.run()