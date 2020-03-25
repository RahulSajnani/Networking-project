import socket
from _thread import *
import threading



if __name__ == "__main__":
    
    # AF_INET refers to the address family ipv4. The SOCK_STREAM means connection oriented TCP protocol.
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host_ip = '127.0.0.1'
    port_number = 13000
    server_socket.bind((host_ip, port_number))

    while True:

        # Listen for clients
        server_socket.listen()

        # Accepting connection with client
        client_socket, client_ip  = server_socket.accept()

        print(client_socket, client_ip)

        client_socket.close()


