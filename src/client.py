import socket
import config

if __name__ == "__main__":
    
    client_socket = socket.socket()
    host_ip = ''
    port_number = 13000
    client_socket.connect((host_ip, port_number))
    
    msg = client_socket.recv(1024)
    # password = input(msg.decode('utf-8') + '\n')
    password = config.PASSWORD
    client_socket.send(password.encode('utf-8'))
    reply = client_socket.recv(1024)

    if reply.decode('utf-8') == '1':
        print('Authenticated. Welcome!')
        connection = True
    else:
        print('Incorrect password! Disconnecting')
        connection = False

    while connection:
    
        command = input('Write command \n')
        
        client_socket.send(command.encode('utf-8'))
        
        if command == 'quit':
            connection = False

        