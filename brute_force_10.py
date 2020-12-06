import sys
import os
import getopt
import glob
import math

from utils import *
from parse import *
from os.path import *

def brute_solve_10(G, s):
    best = ({}, 10)
    curr = {0: 0,
            1: 1,
            2: 2,
            3: 3,
            4: 4,
            5: 5,
            6: 6,
            7: 7,
            8: 8,
            9: 9}
    val = -math.inf

    for st1 in range(2):
        curr[1] = st1
        for st2 in range(st1 + 2):
            curr[2] = st2
            for st3 in range(st2 + 2):
                curr[3] = st3
                for st4 in range(st3 + 2):
                    curr[4] = st4
                    for st5 in range(st4 + 2):
                        curr[5] = st5
                        for st6 in range(st5 + 2):
                            curr[6] = st6
                            for st7 in range(st6 + 2):
                                curr[7] = st7
                                for st8 in range(st7 + 2):
                                    curr[8] = st8
                                    for st9 in range(st8 + 2):
                                        curr[9] = st9
                                        rooms = max(curr.values()) + 1
                                        if is_valid_solution(curr, G, s, rooms):
                                            happ = calculate_happiness(curr, G)
                                            if happ > val:
                                                best = (dict(curr), rooms)
                                                val = happ

    return best

if __name__ == '__main__':
    inputs = glob.glob('./all_inputs/small-*')
    ttl = len(inputs)
    print(ttl)
    ct = 0
    for input_path in inputs:
        if ct % 50 == 0:
            print("{} out of {}".format(ct, ttl))
        output_path = './all_outputs/' + basename(normpath(input_path))[:-3] + '.out'
        G, s = read_input_file(input_path, 10)
        D, k = brute_solve_10(G, s)
        assert is_valid_solution(D, G, s, k)
        write_output_file(D, output_path)
        ct += 1
