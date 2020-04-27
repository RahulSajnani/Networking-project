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

    def getFileHash(self, command_list):
        
        
        if command_list[1].lower() == 'verify':    
            hash_value = self.client_socket.recv(config.BUFFER_SIZE)
            
            hash_value = hash_value.decode('utf-8')
            hash_value_split = helper_functions.string_split(hash_value)
            
            if len(hash_value_split) == 1:
                # file does not exist
                print('Requested file not present on server.')
                return 0, 0
            else:
                hash_value = hash_value_split[1]
                print('Hash val return: ' + str(hash_value))
                size_file = int(hash_value_split[3])
                print(command_list[2] + ' file hash: ' + hash_value + ' size ' + str(size_file))
                return hash_value, size_file
            
        elif command_list[1].lower() == 'checkall':
            info_string = self.receiveData()

            print(info_string)   
            return 0, 0 

        else:
            info_string = self.receiveData()
            print(info_string)   
            return 0, 0


    def FileDownload(self, command_list, cache = 0):

        
        
        string_to_receive = "Requested file not present in server"
        error_message = "Command error. Usage: FileDownload tcp/udp <filename>"
        
        info = self.client_socket.recv(config.BUFFER_SIZE)
        string_received = info.decode('utf-8')
        

        if string_received == string_to_receive or string_received == error_message:
            print (string_received)
            return None 
        elif len(command_list) == 1:
            print(error_message)
            return None
            
        elif command_list[1].lower() == 'udp' or command_list[1].lower() == 'tcp':
            
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
            # self.client_socket.close()
            elif command_list[1] == 'udp' or command_list[1] == 'UDP':
                udp_socket = ''
                if udp_socket != '':
                    udp_socket.close()
                udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                client_ip = self.client_socket.getsockname()[0]
                # print ("Host", client_ip)
                # print ("Port", self.udp_port)
                udp_socket.bind((client_ip,self.udp_port))
                download, address = udp_socket.recvfrom(config.BUFFER_SIZE)
                filedown = open(path,'wb')
                try:
                    while(download):
                        filedown.write(download)
                        udp_socket.settimeout(5)
                        download, address = udp_socket.recvfrom(config.BUFFER_SIZE)
                        progress.update(len(download))
                except socket.timeout:
                    filedown.close()
                    udp_socket.close()


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
            path = self.cache_directory_path + '/' + command_list[2]
            if os.path.exists(path):
                # hasher = hashlib.md5(open(path,'rb').read()).hexdigest()
                hasher = filehash.FileHash('md5')
                hasher = hasher.hash_file(path)
                command = 'FileHash verify ' + command_list[2].replace(' ', '\\ ')
                hash_value, size = self.decode_command(command)
                
                
                print(hash_value)
                print(hasher)
                

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
                
                command = 'FileHash verify ' + command_list[2]
                hash_value, size = self.decode_command(command)
                print(hash_value+'download')
                if hash_value == 0 and size == 0:
                    return 0

                download_flag = helper_functions.clear_cache( self.cache_directory_path, size, self.cache_size)
                
                if download_flag:
                    command = 'FileDownload tcp ' + command_list[2].replace(' ', '\\ ')
                    print (command)    
                    self.client_socket.send(command.encode('utf-8'))
                    command_list = helper_functions.string_split(command)
                    self.FileDownload(command_list, cache=1)
        else:
            print('Command error. Usage :\nCache verify <filename>\nCache show')
            return None


    def IndexGet(self, command_list):

        string_to_print = ''
        string_to_print = self.receiveData()
        
        if string_to_print == '':
            print('No files to show')
        else:
            print(string_to_print)


    def decode_command(self, command):

        command_list = helper_functions.string_split(command)
        
        if command_list[0].lower() != 'cache':
            self.client_socket.send(command.encode('utf-8'))

        if command_list[0] == 'FileHash':
            
            hash, size = self.getFileHash(command_list)
            return hash, size

        elif command_list[0] == 'FileDownload':
            self.FileDownload(command_list)
            
        elif command_list[0] == 'IndexGet':
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
        # readline.write_history_file(self.history_file)

        while self.connection:
            try:
                command = input('$>')
                # readline.add_history(command)
                readline.write_history_file(self.history_file)
                self.decode_command(command)
            except socket.timeout:
                print("Socket timed out.")
                self.connection = False


if __name__ == "__main__":
    
    client = Client()
    client.run() 