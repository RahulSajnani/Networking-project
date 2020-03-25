import socket
from _thread import *
import threading



if __name__ == "__main__":
    
    # AF_INET refers to the address family ipv4. The SOCK_STREAM means connection oriented TCP protocol.
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # host = socket.gethostname()
    host = '0.0.0.0'
    port_number = 13000
    server_socket.bind((host, port_number))
    # Listen for clients
    server_socket.listen(5)
    
    while True:

        # Accepting connection with client
        client_socket, client_ip  = server_socket.accept()

        print(client_socket, client_ip)

        client_socket.close()


