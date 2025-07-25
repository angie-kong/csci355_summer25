# CSCI 355 Internet Web Technologies
# July 2025
# Angela Kong
# Assignment 06 - Socket Programming II with Multi-Threading (client)

import socket
import threading
import time

# constants for 3-way handshake
SYN = 'SYN'
ACK = 'ACK'
ACKSYN = 'ACK+SYN'
FIN = 'FIN'
ACKFIN = 'ACK+FIN'


# create and execute a function get_from_server(server_addr, server_port, file_name, client_path) that connects to the server, creates a connection using "3-way handshake", request the file, receives the file and writes it out locally in the client_apth (distinct from server_path), and then closes the connection using  a "3-way handshake"
def get_from_server(server_addr, server_port, file_name, client_path):
    s = socket.socket()
    s.connect((server_addr, server_port))
    print('Connected')
    msg_SYN = SYN
    s.send(msg_SYN.encode())
    print('Sending : ' + msg_SYN)
    msg_recv = s.recv(2048).decode()
    print('Received : ' + msg_recv)
    if msg_recv != ACKSYN:
        print(ACKSYN + ' not received. Received ' + msg_recv)
        s.close()
        return
    s.send((ACK + file_name).encode())
    print('Sending : ' + ACK + file_name)
    msg_recv = s.recv(2048).decode()
    print('Received : ' + msg_recv)
    f = open(client_path + file_name, 'w')
    f.write(msg_recv)
    f.close()
    print('Write to file : ' + msg_recv)
    s.send(FIN.encode())
    print('Sending : ' + FIN)
    msg_recv = s.recv(2048).decode()
    print('Received : ' + msg_recv)
    if msg_recv == ACKFIN:
        s.close()


def main():
    server_addr = '127.0.0.1'
    server_port = 12345
    file_name = "file2.txt"
    client_path = "output_"
    get_from_server(server_addr, server_port, file_name, client_path)


if __name__ == "__main__":
    main()