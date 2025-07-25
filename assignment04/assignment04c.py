# CSCI 355 Internet Web Technologies
# July 2025
# Angela Kong
# Assignment 04 - Client-Server Socket Programming

import socket
import sys

# function to determine computer's IP address
def get_host_info():
    hostname = socket.gethostname()
    ip_addr = socket.gethostbyname(hostname)
    return hostname, ip_addr


# function to convert IP Address from “dotted decimal notation” to a 32-bit binary string
def binary_address(ip_addr):
    octets = ip_addr.split(".")
    binary = "".join([str(bin(int(octet)))[2:].zfill(8) for octet in octets])
    return binary


# function to determine if the address is Class A, B, C, D or E by examining the first few bits of the 32-bit string
def addr_type(ip_addr):
    if ip_addr == "127.0.0.1":
        return "Loopback address"
    binary = binary_address(ip_addr)
    if binary[0:1] == "0":
        return "Class A"
    elif binary[0:2] == "10":
        return "Class B"
    elif binary[0:3] == "110":
        return "Class C"
    elif binary[0:4] == "1110":
        return "Class D"
    elif binary[0:4] == "1111":
        return "Class E"
    else:
        return "Class unknown"


# function port_type(port) to determine the type of port number
def port_type(port):
    if 0 <= port <= 1023:
        return "Well-Known"
    elif 1024 <= port <= 49151:
        return "Registered"
    elif 49152 <= port <= 65535:
        return "Dynamic/Private"
    else:
        return "Unknown ports"


# function to connect to any server
# An example script to connect to Google using socket programming in Python
def connect_to_server(server_name, port):
    print()
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket successfully created")
    except socket.error as err:
        print("socket creation failed with error %s" % (err))
    try:
        host_ip = socket.gethostbyname(server_name)
    except socket.gaierror:
        # this means could not resolve the host
        print("there was an error resolving the host")
        sys.exit()
    # connecting to the server
    s.connect((host_ip, port))
    print("the socket has successfully connected to ", server_name , "on port " , port)
    analyze_addr(host_ip, port)
    if server_name != "www.google.com":
        # receive data from the server
        print(s.recv(1024).decode())
    # close the connection
    s.close()


def analyze_addr(ip_addr, port):
    print("Your address is: " + ip_addr)
    binary = binary_address(ip_addr)
    print(binary, len(binary))
    add_type = addr_type(ip_addr)
    print("Your address type is: " + add_type)
    prt_type = port_type(port)
    print("Your port type is: " + prt_type)


def main():
    hostname, ip_addr = get_host_info()
    print("Your Computer Name is: " + hostname)
    print("Your Computer IP Address is: " + ip_addr)
    analyze_addr(ip_addr, 1000)
    connect_to_server("www.google.com", 80)
    connect_to_server("djxmmx.net", 17)
    connect_to_server("time-a-g.nist.gov", 13)
    connect_to_server("localhost", 12345)


if __name__ == "__main__":
    main()
