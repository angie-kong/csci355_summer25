# CSCI 355 Internet Web Technologies
# July 2025
# Angela Kong
# Assignment 10 - Data Compression

import heapq
import random

# Class to represent huffman tree
class Node:
    def __init__(self, x):
        self.data = x
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.data < other.data

def dc_run_length_encoding(input, zeros_only = False): # DONE
    output = ""
    n = len(input)
    i = 0
    while i < n- 1:
        count = 1
        while i < n - 1 and input[i] == input[i+1]:
            count += 1
            i += 1
        i += 1

        if not zeros_only:
            output += input[i-1] + str(count) + " "
        elif input[i-1] == "0":
            output += str(count) + " "
        elif input[i-1] == "1":
            output += "0" + " "
    return output

# function to traverse tree in preorder and push huffman rep of each character
def preorder(root, ans, curr):
    if root is None:
        return
    # leaf node = character
    if root.left is None and root.right is None:
        ans.append(curr)
        return
    preorder(root.left, ans, curr + '0')
    preorder(root.right, ans, curr + '1')

# helper function to scramble string
def scramble_string(input_string):
    char_list = list(input_string)
    random.shuffle(char_list)
    scrambled = "".join(char_list)
    return scrambled

def dc_huffman_coding(input, alphabet, freq): # DONE
    s = "".join(alphabet)
    n = len(alphabet)

    # Min heap for node class.
    pq = []
    for i in range(n):
        tmp = Node(freq[i])
        heapq.heappush(pq, tmp)

    # Construct huffman tree.
    while len(pq) >= 2:
        # Left node
        l = heapq.heappop(pq)

        # Right node
        r = heapq.heappop(pq)

        newNode = Node(l.data + r.data)
        newNode.left = l
        newNode.right = r

        heapq.heappush(pq, newNode)

    root = heapq.heappop(pq)
    ans = []
    preorder(root, ans, "")
    # give you code for each char in the input
    encoded = "".join([ans[alphabet.index(c)] for c in input])
    # compression ratio = len of uncompressed * bits needed / compressed
    compression_ratio = len(input) * 3 / len(encoded)
    print("Compression ratio: ", compression_ratio)
    return alphabet, ans, encoded

def dc_lempel_ziv_welch(uncompressed, alphabet): # DONE
        if alphabet:
            dict_size = len(alphabet)
            dictionary = dict((alphabet[i], i) for i in range(dict_size))
        else:
            dict_size = 256
            dictionary = dict((str(chr(i)), i) for i in range(dict_size))
        # in Python 3: dictionary = {chr(i): i for i in range(dict_size)}
        w = ""
        result = []
        for c in uncompressed:
            wc = w + c
            if wc in dictionary:
                w = wc
            else:
                result.append(dictionary[w])
                # Add wc to the dictionary.
                dictionary[wc] = dict_size
                dict_size += 1
                w = c
        if w:
            result.append(dictionary[w])
        return result

# TODO
def compute_cum_freqs(freqs):
    cum_freqs = [0]
    cum_freq = 0
    for i, freq in enumerate(freqs):
        if i == len(freqs) - 1:
            break
        cum_freq += freq
        cum_freqs.append(cum_freq)
    print(cum_freqs)
    return cum_freqs

def dc_arithmetic_encoding(input, chars, freqs, cum_freqs):
    interval0 = 0
    interval1 = 1
    for char in input:
        idx = chars.index(char)
        freq = freqs[idx]
        cum_freq = cum_freqs[idx]
        interval_size = interval1 - interval0
        interval0 += interval_size * cum_freq
        interval1 = interval0 + freq * interval_size
    return interval_to_binary(interval0, interval1)

def interval_to_binary(interval_start, interval_finish):
    bin_str = ""
    prob = 0
    index = 0
    while prob < interval_start:
        index += 1
        power = 1/(2**index)
        if prob + power <= interval_finish:
            bin_str += "1"
            prob += power
        else:
            bin_str += "0"
    print("prob", prob)
    print("bin_string", bin_str)
    return bin_str


def main():
    rl_1 = "AABBCC"
    rl_2 = "00000000000010001100000000"
    print("Run length encoding 1:", dc_run_length_encoding(rl_1, False))
    print("Run length encoding 2:", dc_run_length_encoding(rl_2, True))

    lzw_in = "BAABABBBAABBBBAA"
    print("LZW encoding: ", dc_lempel_ziv_welch(lzw_in, ["A", "B"]))

    hc_in = "A" * 20 + "B" * 10 + "C" * 10 + "D" * 30 + "E" * 30
    freqs = [20, 10, 10, 30, 30]
    alphabet = ["A", "B", "C", "D", "E"]
    hc_in = "".join([alphabet[i] * freqs[i] for i in range(len(freqs))])
    hc_in = scramble_string(hc_in)
    print("Huffman Endcoding: ", dc_huffman_coding(hc_in, alphabet, freqs))
    hc_in = "".join([alphabet[i] * freqs[i] for i in range(len(freqs))])

    message = "BBAB*"
    chars = ["A", "B", "*"]
    freqs = [.4, .5, .1]
    terminating = chars[-1]
    cum_freqs = compute_cum_freqs(freqs)
    print("Arithmetic Endcoding: ", dc_arithmetic_encoding(message, chars, freqs, cum_freqs))

if __name__ == "__main__":
    main()