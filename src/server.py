# server.py

import socket
from _thread import *
import threading
import sys
import config

import filehash
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
            
            if len(command_list) >= 2:
                if command_list[1].lower() == "shortlist" and (len(command_list) == 4 or len(command_list) == 5):

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
                            
                elif command_list[1].lower() == 'longlist' and (len(command_list) == 4 or len(command_list) == 2):
                        
                    if entry.is_dir() == True:
                        string = entry.name + " | Directory | " + file_time + " | " + str(size)

                    elif len(command_list) == 4:
                        if entry.name.lower().endswith(('.txt')):
                            string_to_search = command_list[3]
                            if command_list[2].lower().endswith(('.txt')):    
                                if helper_functions.string_search_txt(self.file_storage_path + "/" + entry.name, string_to_search) == 1:
                                    string = entry.name + " | Text | " + file_time + " | " + str(size)
                
                    elif len(command_list) == 2:
                        if entry.name.lower().endswith(('.pdf')):
                            string = entry.name + " | PDF | " + file_time + " | " + str(size)

                        elif entry.name.lower().endswith(('.jpg', '.jpeg', '.png')):
                            string = entry.name + " | Image | " + file_time + " | " + str(size)

                        elif entry.name.lower().endswith(('.txt')):
                            string = entry.name + " | Text | " + file_time + " | " + str(size)
                

            else:
                error_message = 'Command error.\n Usage: \nIndexGet shortlist 2020:04:29\\ 06:30:01 2020:05:29\\ 06:30:01 (*.txt or *.pdf or *.png or *.jpg)\
                     \n IndexGet longlist (*.txt Programmer) \
                     \n Note: Arguments in brackets are optional.'

                client_socket.send(error_message.encode('utf-8'))
                return None

            if len(string) > 0:
                string_to_send = string_to_send + string + '\n'
        print(string_to_send)
        if string_to_send == '':
            string_to_send = 'No files to display'
        client_socket.send(string_to_send.encode('utf-8'))

    def sendFile(self, client_socket, command_list):
        '''
        Function to send files to client(client download file)

        Input:
            arg - TCP or UDP
            client_socket - client socket object
            filename - filename to the respective file
        Returns:
            None 
        '''

        if len(command_list) == 3:

            if command_list[1].lower() != 'udp' and command_list[1].lower() != 'tcp':
                print('arg error')
                string_to_send = 'Command error. Usage: FileDownload tcp/udp <filename>'
                client_socket.send(string_to_send.encode('utf-8'))
                return None
            
            path = self.file_storage_path+'/'+ command_list[2]
            arg = command_list[1]
            
            string_to_send = "Requested file not present in server"
            if not os.path.isfile(path):
                print (string_to_send)
                client_socket.send(string_to_send.encode('utf-8'))
            else:
                filename = command_list[2]
                file_stats = os.stat(path)
                size = file_stats.st_size
                file_mtime = time.localtime(os.path.getmtime(path))
                file_mtime = time.strftime('%Y-%m-%d %H:%M:%S',file_mtime) 
                hasher = filehash.FileHash('md5')
                hasher = hasher.hash_file(path)
                print ("Sending...")
                file_info_text = ("Filename: %s, Timestamp: %s, MD5hash: %s, Filesize(Bytes): %s" % (filename, str(file_mtime), str(hasher), str(size)))
                print (file_info_text)
                # string_to_send = "Requested file has been found. Filesize: " + str(size)
                string_to_send = "Requested file has been found.\n" + file_info_text 

                print (string_to_send)
                client_socket.send(string_to_send.encode('utf-8'))

                time.sleep(0.02)
                
                if arg == 'tcp' or arg == 'TCP':
                    file = open(path, 'rb')
                    reading = file.read(config.BUFFER_SIZE)
                    # print (reading)
                    while (reading):
                        client_socket.send(reading)
                        reading = file.read(config.BUFFER_SIZE)

                        # print (reading)
                    file.close()
                    
                elif arg == 'udp' or arg == 'UDP':
                    
                    file = open(path, 'rb')
                    client_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    
                    client_ip = client_socket.getpeername()[0]
                    port_number = client_socket.getpeername()
                    
                    if client_ip == '':
                        client_ip = '127.0.0.1'

                    reading = file.read(config.BUFFER_SIZE)

                    while(reading):
                        if (client_udp_socket.sendto(reading,(client_ip, self.udp_port))):
                            reading = file.read(config.BUFFER_SIZE)
                            time.sleep(0.02)
                    client_udp_socket.close()
                    file.close()
        else:
            string_to_send = 'Command error. Usage: FileDownload tcp/udp <filename>'
            client_socket.send(string_to_send.encode('utf-8'))
            return None

    def getFileHash(self, client_socket, command_list):
        '''
        Function to get file hash and send a response to the client
        check deocde_command for info of how this will be called.
        Input:
            client_socket - client socket object
            command_list - list object
        Returns:
            None
        '''

        if len(command_list) == 3 or len(command_list) == 2:
            arg = command_list[1].lower()
            if arg.lower() == 'verify':
                filename = command_list[2]
                if os.path.isfile(self.file_storage_path + '/' + filename):
                    arg_file = open(self.file_storage_path + '/' + filename, 'rb')
                    file_stats = os.stat(self.file_storage_path + '/' + filename)
                    size = file_stats.st_size
                    file_mtime = time.localtime(os.path.getmtime(self.file_storage_path + '/' + filename))
                    file_mtime = time.strftime('%Y-%m-%d %H:%M:%S',file_mtime) 
                    # hasher = hashlib.md5(arg_file.read()).hexdigest()
                    hasher = filehash.FileHash('md5')
                    hasher = hasher.hash_file(self.file_storage_path + '/' + filename)
                    
                    return_value = 'hash: ' + hasher + ' size: ' + str(size) + ' last modified: ' + file_mtime
                    print(return_value)
                    client_socket.send(return_value.encode('utf-8'))
                    return None

                else:
                    return_value = '0'
                    client_socket.send(return_value.encode('utf-8'))
                    return None

            elif arg.lower() == 'checkall':
                
                return_value = ''
                for file_name in os.listdir(self.file_storage_path):
                    
                    hasher = filehash.FileHash('md5')
                    hasher = hasher.hash_file(self.file_storage_path + '/' + file_name)
                    file_mtime = time.localtime(os.path.getmtime(self.file_storage_path + '/' + file_name))
                    file_mtime = time.strftime('%Y-%m-%d %H:%M:%S',file_mtime)
                    return_value = return_value + file_name + ' hash value: ' + hasher + '  last modified:  ' + file_mtime + '\n'
                  
                client_socket.send(return_value.encode('utf-8'))
            
                return None
            
        
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
        
        try:            
            client_loop = True
            while client_loop:

                command = client_socket.recv(config.BUFFER_SIZE)
                
                if command == b'':
                    client_loop = False
                    client_socket.close()

                command = command.decode('utf-8')
                command_list = helper_functions.string_split(command)

                if command_list[0] == 'FileHash':
                    # error handling done
                    self.getFileHash(client_socket, command_list)

                elif command_list[0] == 'FileDownload':
                    # error handling done
                    self.sendFile(client_socket, command_list)

                elif command_list[0] == 'IndexGet':
                    # error handling done
                    self.displayFiles(client_socket, command_list)

                
                elif command_list[0] == 'quit':
                    client_loop = False
                    print('client closed')
                    client_socket.close()

        except socket.timeout:
            print('Client socket timeout. Disconnected.')
            client_socket.close()

        except:
            print('Internal error.')
            client_socket.close()
    
    def run(self):
        '''
        Runs server
        Input: 
            None
        Returns:
            None
        
        '''
        print('Server running')
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
                    print('Client with ip: ' + str(client_ip[0]) + ' connected')
                    self.client_session(client_socket)
                    
                    
if __name__ == "__main__":
    
    server = Server()
    server.run()