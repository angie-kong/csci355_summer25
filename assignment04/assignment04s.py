# CSCI 355 Internet Web Technologies
# July 2025
# Angela Kong
# Assignment 04 - Client-Server Socket Programming

# import the socket library
import socket

# create a socket object
s = socket.socket()
print("Socket successfully created")

# reserve a port on your computer in our case it is 12345 but it can be anything
port = 12345

# Next, bind to the port, but no IP so we can listen to requests from anywhere
s.bind(('', port))
print("socket binded to %s" % (port))

# put the socket into listening mode
s.listen(5)
print("socket is listening")

# a forever loop until we interrupt it or an error occurs
while True:
    # Establish connection with client.
    c, addr = s.accept()
    print('Got connection from', addr)

    # send a thank you message to the client.
    c.send('Thank you for connecting'.encode())

    # Close the connection with the client
    c.close()
