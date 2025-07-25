# CSCI 355 Internet Web Technologies
# July 2025
# Angela Kong
# Assignment 06 - Socket Programming II with Multi-Threading (server)

import socket
import threading
import time

# constants for 3-way handshake
SYN = 'SYN'
ACK = 'ACK'
ACKSYN = 'ACK+SYN'
FIN = 'FIN'
ACKFIN = 'ACK+FIN'

# function to handle resending the file after a certain amount of elapsed time
def send_again_check(c, addr, has_received, msg, timeout = 10):
    old_time = time.time()
    while not has_received[0]:
        if time.time() - old_time >= timeout:
            c.send(msg.encode())
            print(str(addr) + ' Sending again : ' + msg)
            break

# function to handle each client connection
def each_connection(c, addr):
    print(str(addr) + ' Connected')
    is_finishing = False
    has_received = [False]
    while True:
        msg_recv = c.recv(2048).decode()
        has_received[0] = True
        if msg_recv == SYN: # syn request, send ack + syn request back
            print(str(addr) + ' Received : ' + msg_recv)
            msg_send = ACKSYN
            c.send(msg_send.encode())
            print(str(addr) + ' Sending : ' + msg_send)
        elif msg_recv.startswith(ACK) and not is_finishing: # ack but not finished
            print(str(addr) + ' Received : ' + msg_recv)
            file_name = msg_recv[3:]
            if len(file_name) > 0:
                f = open(file_name, 'r')
                file_content = f.read()
                f.close()
                print(str(addr) + ' File contents read')
                c.send(file_content.encode())
                print(str(addr) + ' Sending : ' + file_content)
                has_received[0] = False
                threading.Thread(target=send_again_check, args=(c, addr, has_received, file_content,)).start()
        elif msg_recv == FIN: # fin, want to close connection
            print(str(addr) + ' Received : ' + msg_recv)
            msg_send = ACKFIN
            c.send(msg_send.encode())
            print(str(addr) + ' Sending : ' + msg_send)
            is_finishing = True
        elif msg_recv == ACK and is_finishing:
            break
        else:
            break
    c.close()
    print(str(addr) + ' Connection closed')

# function main to manage the overall server activity
def main():
    s = socket.socket()
    print("Socket successfully created")
    port = 12345
    s.bind(('', port))
    print("Socket binded to %s" % (port))
    s.listen(5)
    print("Socket is listening")
    while True:
        c, addr = s.accept()
        threading.Thread(target=each_connection, args=(c, addr,)).start()
    s.close()


if __name__ == "__main__":
    main()