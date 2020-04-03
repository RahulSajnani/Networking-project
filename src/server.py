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
        self.run_server = False
        self.file_storage_path = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), './file-storage/'))
        
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

    def displayFiles(self, command_list):
        '''
        Function to display files present in server.
        Output: List of Files
        TODO:
            - Get the files from folder with the files
            - Put them in a list
        Input:
            start_time - start time for txt/pdf
            end_time - end time for txt/pdf
            arg - 
            files - file directory
        '''

        if command_list[1] == "longlist":
            
            if len(command_list) < 5:
                files = os.scandir(self.file_storage_path)
                string_to_send = ''
                for entry in files:
                    stats_entry = entry.stat()
                    
                    mtime = time.strftime('%Y-%m-%d::%H:%M:%S', time.localtime(stats_entry.st_mtime))
                    size = stats_entry.st_size

                    if entry.is_dir() == True and (mtime > command_list[2]):
                        string = entry.name + " | Directory | " + " | " + mtime + " | " + size
                        print(entry.name, entry.is_file())
                    elif entry.is_dir() == True and (mtime > command_list[2]):
                        string = entry.name + " | File | " + " | " + mtime + " | " + size
                    
                    string_to_send = string_to_send + entry.name + '|Directory|' 
                pass
            

            pass
        elif command_list[1] == "shortlist":
            
            pass





        pass

    def sendFile(self, client_socket, arg, filename):
        '''
        Function to send files to client(client download file)
        Output : should contain the filename , filesize ,
        lastmodified timestamp and the MD5hash of the
        requested file.
        TODO:
            - Get the file
            - Send the file to client
        Input:
            arg - TCP or UDP
            client_socket - client socket object
            filename - filename to the respective file
        Returns:
            None 
        '''
        # print (self.file_storage_path)
        ###########
        ## CHECK IF FILE EXISTS FIRST!!!!! 
        path = self.file_storage_path+'/'+filename
        if arg == 'tcp' or arg == 'TCP':
            file = open(path, 'rb')
            reading = file.read(1024)
            # print (reading)
            while (reading):
                client_socket.send(reading)
                print (reading)
                reading = file.read(1024)

                # print (reading)
            file_stats = os.stat(path)
            file_mtime = time.localtime(os.path.getmtime(path))
            file_mtime = time.strftime('%Y-%m-%d %H:%M:%S',file_mtime) 
            file.close()
            hasher = hashlib.md5(open(path,'rb').read()).hexdigest()
            print ("Sending...")
            print ("Filename:%s, Filesize(Bytes):%s,Timestamp:%s,MD5hash:%s"%(filename,str(file_stats.st_size),str(file_mtime), str(hasher)))
            
        if arg == 'udp' or arg == 'UDP':
            file = open(filename, 'rb')
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
            client_ip = client_socket.getpeername()[0]
            port_number = client_socket.getpeername()[1]
            
            client_socket.sendto(b'filename',(client_ip, port_number))
            reading = file.read(1024)
            while(reading):
                if (client_socket.sendto(reading,(client_ip, port_number))):
                    reading = file.read(1024)
            file_stats = os.stat(filename)
            file_mtime = time.localtime(os.path.getmtime(filename))
            file_mtime = time.strftime('%Y-%m-%d %H:%M:%S',file_mtime) 
            hasher = hashlib.md5(open(filename,'rb').read()).hexdigest()
            print ("Sending...")
            print ("Filename:%s, Filesize(Bytes):%s,Timestamp:%s,MD5hash:%s"%(filename,str(file_stats.st_size),str(file_mtime), str(hasher)))
            file.close()


           
    
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

        if arg == 'verify':
            arg_file = open(self.file_storage_path + '/' + filename, 'rb')
            hasher = hashlib.md5(arg_file.read()).hexdigest()
            print(filename + ' Hash: ' + hasher)
            
            client_socket.send(hasher.encode('utf-8'))
            pass
        
        elif arg == 'checkall':
            
            string_to_send = ''
            for file_name in os.listdir(self.file_storage_path):
                
                file_ptr = open(self.file_storage_path + '/' + file_name, 'rb')
                hasher = hashlib.md5(file_ptr.read()).hexdigest()
                string_to_send = string_to_send + file_name + ' hash value: ' + hasher + '\n'
            
            
            client_socket.send(string_to_send.encode('utf-8'))

                
            pass
        

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
            
            if command == b'':
                client_loop = False
                client_socket.close()

            command = command.decode('utf-8')
            
            command_list = command.split(' ')
            print(command_list)

            if command_list[0] == 'FileHash':

                if command_list[1] == 'verify':
                    self.getFileHash(client_socket, command_list[1], command_list[2])
                    
                elif command_list[1] == 'checkall':
                    self.getFileHash(client_socket, command_list[1])


            elif command_list[0] == 'FileDownload':
                self.sendFile(client_socket, command_list[1], command_list[2])

                

            elif command_list[0] == 'IndexGet':

                if command_list[1] == 'shortlist':
                    self.displayFiles(command_list)
                elif command_list[1] == 'longlist':
                    self.displayFiles(command_list)
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
        
        self.run_server = True
        client_socket = None

        while self.run_server:

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