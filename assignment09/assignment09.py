# CSCI 355 Internet Web Technologies
# July 2025
# Angela Kong
# Assignment 09 - Error Detection and Correction

from random import random


# [1a] Define a function random_bits(n, p=0.5) that computes a random bit string of length n. The additional, optional parameter p specifies the probability of generating a 1, defaulted to 0.5
def random_bits(n, p=0.5):
    return "".join(['1' if random() < p else "0" for _ in range(n)])

# [1b] Define a function invert_bits(bits, pattern) that inverts the bits where the correspond position in pattern has a 1.
def invert_bits(bits, pattern):
    s = ""
    for i in range(len(bits)):
        if pattern[i] == "1":
            if bits[i] == "0":
                s += "1"
            elif bits[i] == "1":
                s += "0"
        elif pattern[i] == "0":
            s += bits[i]
    return s


# [1c] Define a function random_errors_p(bits, p=0.0) that takes a bit string and for each bit, inverts it with probability p. (With  p=0.0, no bits are inverted.) Suggestion:: use random_bits() to compute an error string and then invert bits.
def random_errors(bits, p=0.0):
    pattern = "".join(['1' if random() < p else "0" for _ in range(len(bits))])
    return invert_bits(bits, pattern)

# [2f] Define a function encode_repetition(bits, copies=3)
# https://en.wikipedia.org/wiki/Repetition_code
# https://en.wikipedia.org/wiki/Majority_logic_decoding
def encode_repetition(bits, copies=3):
    return bits*copies

def majority_logic_decoding(bits, copies=3):
    bb = chop_bits(bits, copies)
    s = ""
    for i in range(len(bb[0])):
        n_1 = 0
        n_0 = 0
        for j in range(copies):
            if bb[j][i] == "1":
                n_1 += 1
            elif bb[j][i] == "0":
                n_0 += 1
        if n_1 > n_0:
            s += "1"
        else:
            s += "0"
    return s


def chop_bits(bits, rows):
    bb = []
    n = len(bits) // rows
    for i in range(rows):
        bb.append(bits[i * n:(i + 1) * n])
    return bb


# [2a] Define a function encode_parity_1d(bits, even=True) that implements the 1D parity check.
#
# See KR - Ch. 6, Slide 13
# https://en.wikipedia.org/wiki/Parity_bit
# https://www.geeksforgeeks.org/error-detection-codes-parity-bit-method/
def encode_parity_1d(bits, even=True):
    n_1 = bits.count("1")
    odd = not even
    return "0" if (even and n_1 % 2 == 0) or (odd and n_1 % 2 == 1) else "1"

# [2b] Define a function encode_parity_2d(bits, rows=-1, cols=-1) that implements the 2D parity check.
#
# See KR - Ch. 6, Slide 13
#
# https://en.wikipedia.org/wiki/Parity_bit
# https://en.wikipedia.org/wiki/Multidimensional_parity-check_code
# https://gaia.cs.umass.edu/kurose_ross/interactive/2d_parity.php
def encode_parity_2d(bits, even=True, rows=-1, cols=-1):
    n = len(bits)
    if rows == -1:
        rows = 2
        cols = n//2
    bb = chop_bits(bits, rows)
    row_parities = "".join([encode_parity_1d(b, even) for b in bb])
    bb_transpose = ["".join([bb[i][j] for i in range(cols)]) for j in range(rows)]
    col_parities = "".join([encode_parity_1d(b, even) for b in bb_transpose])
    return row_parities, col_parities

# [2c] Define a function encode_checksum(bits, ws=16) that implements the Checksum, by breaking the string into words of length word_size (ws).
#
# See KR, Ch. 3, Slides 36-39; Ch. 6, Slide 14
# https://en.wikipedia.org/wiki/Checksum
# https://www.geeksforgeeks.org/computer-networks/error-detection-code-checksum/
def encode_checksum(bits, ws=16):
    rows = len(bits)//ws
    bb = chop_bits(bits, rows)
    c = 0 # carry
    s = 0 # sum
    ss = ""
    for i in range(len(bb[0])-1, -1, -1):
        x = int(bb[0][i])
        y = int(bb[1][i])
        if x+y+c > 1:
            c = 1
        else:
            c= 0
        if x+y+c == 3 or x+y+c == 1:
            s = 1
        else:
            s = 0
        ss = str(s) + ss
    ones_complement = invert_bits(ss, "1"*len(bb[0]))
    return ones_complement

# [2d] Define a function encode_crc(bits) that implements the Cyclic Redundancy Check.
#
# See KR, Ch. 6, Slides 15-16
# https://en.wikipedia.org/wiki/Cyclic_redundancy_check
# https://www.geeksforgeeks.org/cyclic-redundancy-check-python/
# https://www.geeksforgeeks.org/modulo-2-binary-division/

def xor(a, b):
    result = []
    for i in range(1, len(b)):
        if a[i] == b[i]:
            result.append('0')
        else:
            result.append('1')
    return ''.join(result)


def mod2div(dividend, divisor):
    pick = len(divisor)
    tmp = dividend[0: pick]
    while pick < len(dividend):
        if tmp[0] == '1':
            tmp = xor(divisor, tmp) + dividend[pick]
        else:
            tmp = xor('0' * pick, tmp) + dividend[pick]
        # increment pick to move further
        pick += 1
    if tmp[0] == '1':
        tmp = xor(divisor, tmp)
    else:
        tmp = xor('0' * pick, tmp)
    checkword = tmp
    return checkword


def encode_crc(bits, key):
    l_key = len(key)
    appended_data = bits + '0' * (l_key - 1)
    remainder = mod2div(appended_data, key)
    codeword = bits + remainder
    return codeword

# [2e] Define a function encode_hamming(bits) that implements the Hamming Code
#
# https://en.wikipedia.org/wiki/Hamming_code
# https://www.geeksforgeeks.org/hamming-code-in-computer-network/
# https://www.geeksforgeeks.org/hamming-code-implementation-in-c-cpp/
# https://www.geeksforgeeks.org/python/hamming-code-implementation-in-python/
def calcRedundantBits(m):
    # Use the formula 2 ^ r >= m + r + 1 to calculate the no of redundant bits. Iterate over 0 .. m and return the value that satisfies the equation
    for i in range(m):
        if 2**i >= m + i + 1:
            return i


def posRedundantBits(data, r):
    # Redundancy bits are placed at the positionswhich correspond to the power of 2.
    j = 0
    k = 1
    m = len(data)
    res = ''
    # If position is power of 2 then insert '0', Else append the data
    for i in range(1, m + r+1):
        if i == 2**j:
            res = res + '0'
            j += 1
        else:
            res = res + data[-1 * k]
            k += 1
    # The result is reversed since positions are, counted backwards. (m + r+1 ... 1)
    return res[::-1]


def calcParityBits(arr, r):
    n = len(arr)
    # For finding rth parity bit, iterate over 0 to r - 1
    for i in range(r):
        val = 0
        for j in range(1, n + 1):
            # If position has 1 in ith significant position then Bitwise OR the array value to find parity bit value.
            if j & (2**i) == (2**i):
                val = val ^ int(arr[-1 * j])
                # -1 * j is given since array is reversed
        # String Concatenation (0 to n - 2^r) + parity bit + (n - 2^r + 1 to n)
        arr = arr[:n-(2**i)] + str(val) + arr[n-(2**i)+1:]
    return arr


def detectError(arr, nr):
    n = len(arr)
    res = 0
    # Calculate parity bits again
    for i in range(nr):
        val = 0
        for j in range(1, n + 1):
            if(j & (2**i) == (2**i)):
                val = val ^ int(arr[-1 * j])
        # Create a binary no by appending parity bits together.
        res = res + val*(10**i)
    # Convert binary to decimal
    return int(str(res), 2)


def encode_hamming(bits):
    # Calculate the no of Redundant Bits Required
    m = len(bits)
    r = calcRedundantBits(m)
    # Determine the positions of Redundant Bits
    arr = posRedundantBits(bits, r)
    # Determine the parity bits
    arr = calcParityBits(arr, r)
    return arr


def main():
    n = 16
    bits = random_bits(n)
    print("Bits:                  ", bits)
    print("Invert first two bits: ", invert_bits(bits, "1"*2 + "0"*14))
    print("Invert random bits:    ", random_errors(bits, 0.25))
    bits_rep = encode_repetition(bits, 3)
    print("Repetition bits:       ", bits_rep)
    bits_rep_err = random_errors(bits_rep, 0.1)
    bits_rep_mld = majority_logic_decoding(bits_rep_err)
    print("Major logic decoding:  ", bits_rep_mld)
    print("Parity 1D: (even)      ", encode_parity_1d(bits, even=True))
    print("Parity 1D: (odd)       ", encode_parity_1d(bits, even=False))
    print("Parity 2D: (even)      ", encode_parity_2d(bits, even=True, rows=4, cols=4))
    print("Checksum:              ", encode_checksum(bits, 8))
    print("CRC: key = 1001        ", encode_crc(bits, "1001"))
    print("Hamming code:          ", encode_hamming(bits))

if __name__ == "__main__":
    main()