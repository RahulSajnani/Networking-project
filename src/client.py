import socket
import config

class Client:

    def __init__(self):

        self.client_socket = socket.socket()
        self.host_ip = ''
        self.port_number = 13000
        self.connection = False

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

        

    def decode_command(self, command):

        command_list = command.split(' ')
        self.client_socket.send(command.encode('utf-8'))

        if command_list[0] == 'FileHash':
            
            if command_list[1] == 'verify':    
                reply = self.client_socket.recv(1024)
                reply = reply.decode('utf-8')
                print(command_list[2] + ' file hash: ' + reply)


        elif command_list[0] == 'quit':
            self.connection = False
        pass
    
    def run(self):

        # Authenticates client
        self.authenticate()
        
        while self.connection:

            command = input('Write command \n')
            self.decode_command(command)
            
            
        pass


if __name__ == "__main__":
    
    client = Client()
    client.run() 