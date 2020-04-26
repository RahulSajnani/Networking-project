# server.py
import socket
from _thread import *
import threading
import sys
import config
import hashlib
import os
import time
import helper_functions
import tqdm
from datetime import datetime, date

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
        self.udp_port = 6000
        self.cache_directory_path = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), './client-cache/'))

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

    def displayFiles(self, client_socket, command_list):
        '''
        Function to display files present in server. INDEXGET command
        Output: List of Files
        TODO:
            - Get the files from folder with the files
            - Put them in a list
        Input:
            client_socket - socket object - client socket
            command_list - list - list of command separated with space ( escaped with '\ ')
        '''

            
        files = os.scandir(self.file_storage_path)
        string_to_send = ''
        for entry in files:
            stats_entry = entry.stat()

            mtime = time.localtime(stats_entry.st_mtime)
            mtime = datetime(*mtime[:6])
            size = stats_entry.st_size

            # print(mtime, '\n', start_time,'\n', end_time)
            file_time = mtime.strftime("%Y-%m-%d %H:%M:%S")
            string = ''
            
            if command_list[1].lower() == "shortlist":
                start_time = (datetime.strptime(command_list[2], '%Y-%m-%d %H:%M:%S')) 
                end_time = (datetime.strptime(command_list[3], '%Y-%m-%d %H:%M:%S'))
                # print(start_time,'\n', end_time, '\n')
            
                if entry.is_dir() == True and (end_time > mtime) and (mtime > start_time):
                    string = entry.name + " | Directory | " + file_time + " | " + str(size)

                elif ((end_time > mtime) and (mtime > start_time)):
                    
                    if entry.name.lower().endswith(('.pdf')):
                        if len(command_list) == 5:
                            if command_list[4].lower().endswith(('.pdf')):
                                string = entry.name + " | PDF | " + file_time + " | " + str(size)
                        else:
                            string = entry.name + " | PDF | " + file_time + " | " + str(size)

                    elif entry.name.lower().endswith(('.jpg', '.jpeg', '.png')):
                        if len(command_list) == 5:
                            if command_list[4].lower().endswith(('.jpg', '.jpeg', '.png')):
                                string = entry.name + " | Image | " + file_time + " | " + str(size)
                        else:
                            string = entry.name + " | Image | " + file_time + " | " + str(size)

                    elif entry.name.lower().endswith(('.txt')):
                        if len(command_list) == 5:
                            if command_list[4].lower().endswith(('.txt')):
                                string = entry.name + " | Text | " + file_time + " | " + str(size)
                        else:
                            string = entry.name + " | Text | " + file_time + " | " + str(size)
                        
            elif command_list[1].lower() == 'longlist':
                    
                if entry.is_dir() == True:
                    string = entry.name + " | Directory | " + file_time + " | " + str(size)

                else:
                    if entry.name.lower().endswith(('.pdf')):
                        string = entry.name + " | PDF | " + file_time + " | " + str(size)

                    elif entry.name.lower().endswith(('.jpg', '.jpeg', '.png')):
                        string = entry.name + " | Image | " + file_time + " | " + str(size)

                    elif entry.name.lower().endswith(('.txt')):
                        string = entry.name + " | Text | " + file_time + " | " + str(size)
                
                    
            if len(string) > 0:
                string_to_send = string_to_send + string + '\n'
        print(string_to_send)
        if string_to_send == '':
            string_to_send = 'No files to display'
        client_socket.send(string_to_send.encode('utf-8'))

    def sendFile(self, client_socket, command_list):
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


        if len(command_list) == 1:
            string_to_send = 'Command error. Usage: FileDownload tcp/udp <filename>'
            client_socket.send(string_to_send.encode('utf-8'))
            return None
        
        
         
        if command_list[1].lower() != 'udp' and command_list[1].lower() != 'tcp':
            print('arg error')
            string_to_send = 'Command error. Usage: FileDownload tcp/udp <filename>'
            client_socket.send(string_to_send.encode('utf-8'))
            return None

        if command_list[0] == 'FileDownload':
            path = self.file_storage_path+'/'+ command_list[2]
            
            arg = command_list[1]

        string_to_send = "Requested file not present in server"
        filename = command_list[2]
        

        if not os.path.isfile(path):
            print (string_to_send)
            client_socket.send(string_to_send.encode('utf-8'))

        else:
            string_to_send = "Requested file has been found"
            print (string_to_send)
            client_socket.send(string_to_send.encode('utf-8'))

            file_stats = os.stat(path)
            size = file_stats.st_size

            string_to_send = "Filesize: " + str(size)
            client_socket.send(string_to_send.encode('utf-8'))
            print(string_to_send)
            time.sleep(1)
            
            if arg == 'tcp' or arg == 'TCP':
                file = open(path, 'rb')
                reading = file.read(config.BUFFER_SIZE)
                # print (reading)
                while (reading):
                    client_socket.send(reading)
                    reading = file.read(config.BUFFER_SIZE)

                    # print (reading)
                file_stats = os.stat(path)
                file_mtime = time.localtime(os.path.getmtime(path))
                file_mtime = time.strftime('%Y-%m-%d %H:%M:%S',file_mtime) 
                file.close()
                hasher = hashlib.md5(open(path,'rb').read()).hexdigest()
                print ("Sending...")
                print ("Filename:%s, Filesize(Bytes):%s,Timestamp:%s,MD5hash:%s"%(filename,str(file_stats.st_size),str(file_mtime), str(hasher)))
            
            elif arg == 'udp' or arg == 'UDP':
                
                file = open(path, 'rb')
                client_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                
                client_ip = client_socket.getpeername()[0]
                # port_number = client_socket.getpeername()[1]
                print (path)

                
                if client_ip == '':
                    client_ip = '127.0.0.1'
                # Testing:
                # client_socket.sendto(b'filename',(self.host, self.udp_port))
                # print ('Host',client_ip)
                # print ('Port', self.udp_port)
                reading = file.read(config.BUFFER_SIZE)

                while(reading):
                    if (client_udp_socket.sendto(reading,(client_ip, self.udp_port))):
                        reading = file.read(config.BUFFER_SIZE)

                    # if len(reading) < config.BUFFER_SIZE:
                    #     break

                file_stats = os.stat(path)
                file_mtime = time.localtime(os.path.getmtime(path))
                file_mtime = time.strftime('%Y-%m-%d %H:%M:%S',file_mtime)
                hasher = hashlib.md5(open(path,'rb').read()).hexdigest()
                print ("Sending...")
                print ("Filename:%s, Filesize(Bytes):%s,Timestamp:%s,MD5hash:%s"%(filename,str(file_stats.st_size),str(file_mtime), str(hasher)))
                file.close()
                client_udp_socket.close()


           
    
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

        if arg.lower() == 'verify':

            if os.path.isfile(self.file_storage_path + '/' + filename):
                arg_file = open(self.file_storage_path + '/' + filename, 'rb')
                file_stats = os.stat(self.file_storage_path + '/' + filename)
                size = file_stats.st_size
                hasher = hashlib.md5(arg_file.read()).hexdigest()
                print(filename + ' Hash: ' + hasher)
                
                return_value = 'Hash ' + hasher + ' size ' + str(size)
                print(return_value)
                client_socket.send(return_value.encode('utf-8'))
            
            else:
                
                return_value = '0'
                client_socket.send(return_value.encode('utf-8'))
            

        elif arg.lower() == 'checkall':
            
            return_value = ''
            for file_name in os.listdir(self.file_storage_path):
                
                file_ptr = open(self.file_storage_path + '/' + file_name, 'rb')
                hasher = hashlib.md5(file_ptr.read()).hexdigest()
                return_value = return_value + file_name + ' hash value: ' + hasher + '\n'
            
            
            client_socket.send(return_value.encode('utf-8'))

        else:
            return_value = "Command error. Usage: FileHash verify <filename>\n FileHash checkall"
            client_socket.send(return_value.encode('utf-8'))
     

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

            command = client_socket.recv(config.BUFFER_SIZE)
            
            if command == b'':
                client_loop = False
                client_socket.close()

            command = command.decode('utf-8')
            
            command_list = helper_functions.string_split(command)
            print(command_list)

            if command_list[0] == 'FileHash':

                if command_list[1] == 'verify':
                    self.getFileHash(client_socket, command_list[1], command_list[2])
                    
                elif command_list[1] == 'checkall':
                    self.getFileHash(client_socket, command_list[1])


            elif command_list[0] == 'FileDownload':
                self.sendFile(client_socket, command_list)

            elif command_list[0] == 'IndexGet':

                if command_list[1] == 'shortlist':
                    self.displayFiles(client_socket, command_list)
                elif command_list[1] == 'longlist':
                    self.displayFiles(client_socket, command_list)
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
        
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

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
                elif client_socket is not None:
                    self.authenticated_clients.append(client_socket)
                    print(str(client_ip))
                    
                    # client_socket.settimeout(config.SOCKET_TIMEOUT)
                    # try:
                    self.client_session(client_socket)
                    # except:
                    #     print ('client socket timeout')
                    #     client_socket.close()

                    
                        
                        

                        

if __name__ == "__main__":
    
    server = Server()
    
    server.run()