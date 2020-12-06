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
        lst = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        curr[1] = st1
        lst[1] = st1
        for st2 in range(max(lst[:2]) + 2):
            curr[2] = st2
            lst[2] = st2
            for st3 in range(max(lst[:3]) + 2):
                curr[3] = st3
                lst[3] = st3
                for st4 in range(max(lst[:4]) + 2):
                    curr[4] = st4
                    lst[4] = st4
                    for st5 in range(max(lst[:5]) + 2):
                        curr[5] = st5
                        lst[5] = st5
                        for st6 in range(max(lst[:6]) + 2):
                            curr[6] = st6
                            lst[6] = st6
                            for st7 in range(max(lst[:7]) + 2):
                                curr[7] = st7
                                lst[7] = st7
                                for st8 in range(max(lst[:8]) + 2):
                                    curr[8] = st8
                                    lst[8] = st8
                                    for st9 in range(max(lst[:9]) + 2):
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
        if ct % 25 == 0:
            print("{} out of {}".format(ct, ttl))
        output_path = './all_outputs/' + basename(normpath(input_path))[:-3] + '.out'
        G, s = read_input_file(input_path, 10)
        D, k = brute_solve_10(G, s)
        assert is_valid_solution(D, G, s, k)
        write_output_file(D, output_path)
        ct += 1

# if __name__ == '__main__':
#     assert len(sys.argv) == 2
#     path = sys.argv[1]
#     G, s = read_input_file(path)
#     D, k = brute_solve_10(G, s)
#     assert is_valid_solution(D, G, s, k)
#     print("Total Happiness: {}".format(calculate_happiness(D, G)))
#     write_output_file(D, 'out/test.out')
