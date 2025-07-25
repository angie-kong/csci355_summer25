# CSCI 355 Internet Web Technologies
# July 2025
# Angela Kong
# Assignment 07 - Network Addressing and Forwarding

import subprocess
import OutputUtil as ou
from pyroute2 import IPRoute


# function execute_command(cmd) to execute a shell command ("cmd")
def exec_cmd(cmd, arg):
    try:
        result = subprocess.run([cmd, arg, "-l"], capture_output=True, text=True, check=True)
        print("Command Output:")
        # print(result.stdout)
        if result.stderr:
            print("Standard Error:")
            print(result.stderr)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error: {e}")
        print(f"Stderr: {e.stderr}")


# function get_routing_table by using the function from the previous step to run "route print" and then parsing the output into a table (2-D list).
def get_routing_table(routing_data):
    s = routing_data
    s = s[s.find("Destination"): s.find("Internet6") - 1].strip()
    lines = s.split('\n')
    print (lines)
    data = [[get(x,0,17), get(x,18,37), get(x,38,51), get(x,52,69), get(x,70,73), get(x,80, 85), get(x, 86, 90), get(x, 91, 111)] for x in lines]
    headers = data[0]
    data = data[1:]
    for row in data:
        print (row)
    return headers,data


def get(s,i,j):
    return s[i:j+1].strip()

# function validate_address() to validate the address in two ways:
# Call your own function to check that the entered IP address is valid, that is, it consists of four decimal numbers, each between 0 and 255, and separated by dots (periods).
# Call code from socket package to validate it. See https://stackoverflow.com/questions/319279/how-to-validate-ip-address-in-python
def validate_address(address):
    octets = address.split(".")
    if len(octets) != 4:
        return "Address does not contain four octets separated by dots"
    for octet in octets:
        if not octet.isdigit():
            return "Octet found with non-number"
        if int(octet) > 255 or int(octet) < 0:
            return "Octet value out of range 0-255"
    return "Valid IP address"


# function get_binary_address() to  find the binary equivalent of an IP address in dotted decimal notation and use it on the inputted IP address.
def binary_address(ip_addr):
    octets = ip_addr.split(".")
    binary = "".join([str(bin(int(octet)))[2:].zfill(8) for octet in octets])
    return binary


# function get_classful_address_type()
def get_classful_address_type(ip_addr):
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


# function to do the “bitwise-AND” of two bit-strings
def bitwise_and(s1, s2):
    n1 = len(s1)
    n2 = len(s2)
    s = ""
    for i in range(min(n1, n2)):
        s += "1" if s1[i] == "1" and s2[1] == "1" else "0"
    return s + "0" * (abs(n1-n2))


def prefix_match(s1, s2):
    n1 = len(s1)
    n2 = len(s2)
    p = 0
    for i in range(min(n1, n2)):
        if s1[i] != s2[i]:
            return p
        else:
            p += 1
    return p


# [9] Compare the Next Hop to that provided by Python:
def get_python_next_hop(ip_addr):
    with IPRoute() as ipr:
        return ipr.route('get', dst=ip_addr)

# [8] Define a function get_next_hop() to loop through the rows of the routing table from step [2] and determine the “Next Hop” for the user-inputted address. To determine which row is determinant, use the following algorithm:
# Do a bitwise-AND of the network mask with the destination IP address and see if you have a match with “Network Destination”, the first column. Mathematically, this can be expressed at N = D & M where D is the Destination IP address, M is the (network) Mask, and N is the (destination) Network.
# Use the Metric column to decide between multiple matches (lowest value of Metric gets priority)
# If you have multiple matches and the Metric column is the same for all, then use the “Longest Prefix Match” to decide between ties, that is the one with more non-zero bits in the Mask.
def get_next_hop(ip_addr, rt):
    print("Iterating through routing table")
    best_p = 0
    best_row = None
    for row in rt:
        dest = row[0].split("/")
        dest = dest[0]
        if validate_address(dest) == "Valid IP address":
            b_addr = binary_address(ip_addr)
            b_dest = binary_address(dest)
            p = prefix_match(b_addr, b_dest)
            print(ip_addr, row[0], dest, b_addr, b_dest, p)
            if p > best_p:
                best_p = p
                best_row = row
    print("Best routing table row: ", best_row, "Best prefix match: ", best_p)
    print()
    return best_p, best_row


def main():
    netstat_output = exec_cmd("netstat", "-nr")
    headers, data = get_routing_table(netstat_output)
    # abc.def.ghi.jkl # not decimal
    # 111-111-111-111 # not dotted
    # 613.613.613.613 # format correct but numbers out of range
    # 123.123.123 # valid numbers but only three octets
    # 225.225.225.225 # valid address but class D
    # 241.242.243.244 # valid address but class E
    # 127.0.0.1 # valid - loopback address
    # 52.3.73.91 # valid - an address for amazon
    # 216.239.63.255 # valid - an address for google
    addresses = ["abc.def.ghi.jkl", "111-111-111-111", "613.613.613.613", "123.123.123", "225.225.225.225", "241.242.243.244", "127.0.0.1", "52.3.73.91", "216.239.63.255"]
    for address in addresses:
        status = validate_address(address)
        print(address, status)
        if status == "Valid IP address":
            cls = get_classful_address_type(address)
            b_addr = binary_address(address)
            next_hop = get_next_hop(address, data)
            print(address, cls, b_addr)
    types = ["S"] * len(headers)
    alignments = ["l"] * len(headers)
    title = "My Routing Table<br>Angela Kong"
    ou.write_html_file("assignment07.html", title, headers, types, alignments, data, True)


if __name__ == "__main__":
    main()