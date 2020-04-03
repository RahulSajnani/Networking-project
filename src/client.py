import socket
import config
import os
import helper_functions

class Client:

    def __init__(self):

        self.client_socket = socket.socket()
        self.host_ip = ''
        self.port_number = 13000
        self.connection = False
        self.file_storage_path = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), './file-storage-client/'))
        
    def authenticate(self):
        
        self.client_socket.connect((self.host_ip, self.port_number))
        msg = self.client_socket.recv(1024)

        # password = input(msg.decode('utf-8') + '\n')
        password = config.PASSWORD
        self.client_socket.send(password.encode('utf-8'))
        reply = self.client_socket.recv(1024)

        if reply.decode('utf-8') == '1':
            print('Authenticated. Welcome!')
            self.connection = True
        else:
            print('Incorrect password! Disconnecting')
            self.connection = False

    
    def getFileHash(self, command_list):
        
        
        if command_list[1] == 'verify':    
            hash_value = self.client_socket.recv(1024)
            hash_value = hash_value.decode('utf-8')
            print(command_list[2] + ' file hash: ' + hash_value)
            return hash_value
        
        elif command_list[1] == 'checkall':

            info_string = ''
            
            while True:
                
                info = self.client_socket.recv(1024)
                info_string = info_string + info.decode('utf-8')
                if len(info) < 1024:
                    break    

            print(info_string)    



    def FileDownload(self, command_list):
        path = self.file_storage_path+'/' + command_list[2]
        print (path)
        if command_list[1] == 'tcp' or command_list[1] == 'TCP':
            
            with open(path,'wb') as filedown:
                while True:
                    download = self.client_socket.recv(1024)
                    print (download)
                    
                    filedown.write(download)
                    if len(download) < 1024:
                        break
                    
            filedown.close()
        # self.client_socket.close()
        # if command_list[1] == 'udp' or command_list[1] == 'UDP':





    def IndexGet(self, command_list):

        string_to_print = ''
        while True:
            
            info = self.client_socket.recv(1024)
            string_to_print = string_to_print + info.decode('utf-8')
            if len(info) < 1024:
                break
        
        print(string_to_print)


    def decode_command(self, command):

        command_list = helper_functions.string_split(command)
        self.client_socket.send(command.encode('utf-8'))

        if command_list[0] == 'FileHash':
            self.getFileHash(command_list)
        elif command_list[0] == 'FileDownload':
            self.FileDownload(command_list)
            
        elif command_list[0] == 'IndexGet':
            self.IndexGet(command_list)  


        elif command_list[0] == 'quit':
            self.connection = False
        pass
    
    def run(self):

        # Authenticates client
        self.authenticate()
        
        while self.connection:

            command = input('$>')
            self.decode_command(command)
            
            
        pass


if __name__ == "__main__":
    
    client = Client()
    client.run() 