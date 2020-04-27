import socket
import config
import os
import helper_functions
import filehash
import tqdm
import readline

class Client:

    def __init__(self):

        self.client_socket = socket.socket()
        # self.client_socket.settimeout(config.SOCKET_TIMEOUT)
        self.history_file = './history.log'
        self.host_ip = ''
        self.port_number = 13000
        self.connection = False
        self.file_storage_path = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), './file-storage-client/'))
        # hardcoded udp port to be 6000
        self.udp_port = 6000
        self.cache_directory_path = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), './client-cache/'))
        
        self.cache_size = 3 * 1024 * 1024

    def authenticate(self):
        
        self.client_socket.connect((self.host_ip, self.port_number))
        msg = self.client_socket.recv(config.BUFFER_SIZE)

        # password = input(msg.decode('utf-8') + '\n')
        password = config.PASSWORD
        self.client_socket.send(password.encode('utf-8'))
        reply = self.client_socket.recv(config.BUFFER_SIZE)

        if reply.decode('utf-8') == '1':
            print('Authenticated. Welcome!')
            self.connection = True
        else:
            print('Incorrect password! Disconnecting')
            self.connection = False

    def receiveData(self):
        
        info_string = ''
            
        while True:
            
            info = self.client_socket.recv(config.BUFFER_SIZE)
            # print(info)
            info_string = info_string + info.decode('utf-8')
            if len(info) < config.BUFFER_SIZE:
                break    

        return info_string

    # FileHash command
    def getFileHash(self, command_list):
        
       
        if len(command_list) == 3 or len(command_list) == 2:
            if command_list[1].lower() == 'verify':    
                hash_value = self.client_socket.recv(config.BUFFER_SIZE)
                
                hash_value = hash_value.decode('utf-8')
                
                hash_value_split = helper_functions.string_split(hash_value)
                
                if len(hash_value_split) == 1:
                    # file does not exist
                    print('Requested file not present on server.')
                    return 0, 0
                else:
                    print(hash_value)
                    hash_value = hash_value_split[1]
                    size_file = int(hash_value_split[3])
                    return hash_value, size_file
                
            elif command_list[1].lower() == 'checkall':
                info_string = self.receiveData()
                print(info_string)   
                return 0, 0 

        
        info_string = self.receiveData()
        print(info_string)   
        return 0, 0

    # FileDownload command
    def FileDownload(self, command_list, cache = 0):


        if len(command_list) != 3:
            
            error_message = "Command error. Usage: FileDownload tcp/udp <filename>"
            info = self.client_socket.recv(config.BUFFER_SIZE)
            string_received = info.decode('utf-8')
            print(string_received)
        
            
        elif (command_list[1].lower() == 'udp' or command_list[1].lower() == 'tcp'):
            
            string_to_receive = "Requested file not present in server"
            info = self.client_socket.recv(config.BUFFER_SIZE)
            string_received = info.decode('utf-8')

            if string_received == string_to_receive:
                print (string_received)
                return None 
            
            print (string_received)
            if cache:
                path = self.cache_directory_path+'/' + command_list[2]
            else:    
                path = self.file_storage_path+'/' + command_list[2]
            
            size = helper_functions.string_split(string_received)[-1]
            size = int(size)
            print(size)

            progress = tqdm.tqdm(range(size), f"Receiving ", unit="B", unit_scale=True, unit_divisor=config.BUFFER_SIZE)
            if command_list[1] == 'tcp' or command_list[1] == 'TCP':
                
                with open(path,'wb') as filedown:
                    while True:
                        download = self.client_socket.recv(config.BUFFER_SIZE)
                        filedown.write(download)
                        if len(download) < config.BUFFER_SIZE:
                        # if not download:
                            break
                        
                        progress.update(len(download))
                        
                filedown.close()
                print("File Downloaded")

            elif command_list[1] == 'udp' or command_list[1] == 'UDP':
                
                udp_socket = ''
                if udp_socket != '':
                    udp_socket.close()
                udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                client_ip = self.client_socket.getsockname()[0]
                
                udp_socket.bind((client_ip,self.udp_port))
                filedown = open(path,'wb')
                try:
                    udp_socket.settimeout(2)
                    download, address = udp_socket.recvfrom(config.BUFFER_SIZE)
                    while(download):
                        filedown.write(download)
                        udp_socket.settimeout(2)
                        download, address = udp_socket.recvfrom(config.BUFFER_SIZE)
                        progress.update(len(download))

                    print("File Downloaded")
                    
                except socket.timeout:
                    filedown.close()
                    udp_socket.close()
                    print("File Downloaded")

    # Cache command
    def Cache(self, command_list):
        '''
        Cache command
        Input :
            command_list - list object - contains command separated at spaces
        Return :
            None
        '''

        if len(command_list) == 1:
            print('Command error. Usage :\nCache verify <filename>\nCache show')
            return None

        if command_list[1].lower() == 'show':

            files = os.scandir(self.cache_directory_path)
            # print (files)
            string_to_display = ''
            for entry in files:
                stats_entry = entry.stat()
                size = stats_entry.st_size
                string = entry.name + " | " + str(size)
                string_to_display = string_to_display + string + '\n'

            if string_to_display == '':
                string_to_display = 'No files to display'
            
            print(string_to_display)
        
        elif command_list[1].lower() == 'verify':
            download_flag = 1
            file_name = command_list[2]
            file_name = file_name.replace(' ', '\\ ')
            path = self.cache_directory_path + '/' + command_list[2]
            if os.path.exists(path):
                hasher = filehash.FileHash('md5')
                hasher = hasher.hash_file(path)
                command = 'FileHash verify ' + file_name

                hash_value, size = self.decode_command(command)

                if hash_value == 0 and size == 0:
                    download_flag = 0
                    return 0 

                elif hasher == hash_value:
                    print('File exists.')
                    download_flag = 0
                else: 
                    print('File changed on server downloading again.')
                    download_flag = 1
            

            if download_flag:
                
                command = 'FileHash verify ' + file_name
                hash_value, size = self.decode_command(command)
                
                if hash_value == 0 and size == 0:
                    return 0

                download_flag = helper_functions.clear_cache( self.cache_directory_path, size, self.cache_size)
                
                if download_flag:
                    command = 'FileDownload tcp ' + file_name
                    print('Downloading file\n')
                    self.client_socket.send(command.encode('utf-8'))
                    command_list = helper_functions.string_split(command)
                    self.FileDownload(command_list, cache=1)
        else:
            print('Command error. Usage :\nCache verify <filename>\nCache show')
            return None

    # IndexGet command
    def IndexGet(self, command_list):
        
        # if len(command_list) == 3:    
        string_to_print = ''
        string_to_print = self.receiveData()
        
        if string_to_print == '':
            print('No files to show')
        else:
            print(string_to_print)

    # decode logic
    def decode_command(self, command):

        command_list = helper_functions.string_split(command)
        
        if command_list[0].lower() != 'cache':
            self.client_socket.send(command.encode('utf-8'))

        if command_list[0] == 'FileHash':
            # error handling done
            hash, size = self.getFileHash(command_list)
            return hash, size

        elif command_list[0] == 'FileDownload':
            # error handling done
            self.FileDownload(command_list)
            
        elif command_list[0] == 'IndexGet':
            #
            self.IndexGet(command_list)  

        elif command_list[0] == 'Cache':
            self.Cache(command_list)

        elif command_list[0] == 'quit':
            self.connection = False
        
        else: 
            print('Incorrect command')
    
    def run(self):

        # Authenticates client
        self.authenticate()
        
        if not os.path.exists(self.history_file):
            open(self.history_file, 'a').close()
        
        readline.clear_history()
        readline.set_history_length(100)

        while self.connection:
            try:
                command = input('\n$>')
                readline.write_history_file(self.history_file)
                self.decode_command(command)

            except socket.error:

                self.connection = False
                print('Socket timeout')
            
            except:
                self.connection = False
                print('Internal error')
            

if __name__ == "__main__":
    
    client = Client()
    client.run() 