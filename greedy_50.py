import sys
import os
import getopt
import glob
import math
import timeit
import random

import multiprocessing as mp

from utils import *
from parse import *
from os.path import *

ITERATIONS = 10 ** 5

def greedy_solve_50(G, s):
    curr = {}
    rooms = {}

    best_happiness = 0

    for i in range(50):
        curr[i] = 0

    if is_valid_solution(curr, G, s, 1):
        return (curr, 1)

    # for e in list(G.edges.data()):
    #     if e[2]['stress'] > s / 2:
    #         G.remove_edge(*e[:2])

    edgelist = list(G.edges.data())

    edgelist.sort(key = lambda x: -x[2]['happiness'])
    edgelist.sort(key = lambda x: x[2]['stress'])

    for i in range(50):
        curr[i] = i
        rooms[i] = [i]

    best = (dict(curr), 50)

    # print("creating prior...")
    for e in edgelist:
        if e[2]['stress'] > s / 10:
            break
        # print(e)
        # print(rooms)
        # print(curr)
        st1, st2, _ = e
        st1_num, st2_num = curr[st1], curr[st2]
        st1_room, st2_room = rooms[st1_num], rooms[st2_num]

        combined = st1_room + st2_room

        swap_into_st1_1 = st1_room + [st2]
        swap_into_st1_2 = st2_room[:]

        swap_into_st2_1 = st1_room[:]
        swap_into_st2_2 = st2_room + [st1]

        swap_into_st1_2.remove(st2)
        swap_into_st2_1.remove(st1)

        # print(combined)
        # print(swap_into_st1_1, swap_into_st1_2)
        # print(swap_into_st2_1, swap_into_st2_2)

        curr_happ = calculate_happiness_for_room(st1_room, G) + calculate_happiness_for_room(st2_room, G)
        comb_happ = calculate_happiness_for_room(combined, G)
        s_st1_happ = calculate_happiness_for_room(swap_into_st1_1, G) + calculate_happiness_for_room(swap_into_st1_2, G)
        s_st2_happ = calculate_happiness_for_room(swap_into_st2_1, G) + calculate_happiness_for_room(swap_into_st2_2, G)

        if comb_happ >= max([curr_happ, s_st1_happ, s_st2_happ]):
            for st in st2_room:
                curr[st] = st1_num
            rooms[st1_num] = combined
            rooms[st2_num] = []
            # print("combined")

        elif s_st1_happ >= max([curr_happ, comb_happ, s_st2_happ]):
            curr[st2] = st1_num
            rooms[st1_num] += [st2]
            st2_room.remove(st2)
            # print("moved to st1")

        elif s_st2_happ >= max([curr_happ, comb_happ, s_st1_happ]):
            curr[st1] = st2_num
            rooms[st2_num] += [st1]
            st1_room.remove(st1)
            # print("moved to st2")

        # print(curr)
        # print(rooms)
        rooms = reorder_rooms(rooms)
        curr = convert_dictionary(rooms)
        num_rooms = max(curr.values()) + 1
        if is_valid_solution(curr, G, s, num_rooms):
            happ = calculate_happiness(curr, G)
            if happ > best_happiness:
                best_happiness = happ
                best = (dict(curr), num_rooms)

    print(best)
    return best

def reorder_rooms(rooms):
    ret = {}
    count = 0
    for room in rooms.values():
        if room:
            ret[count] = room
            count += 1
    return ret

# if __name__ == '__main__':
#     assert len(sys.argv) == 2
#     path = sys.argv[1]
#     G, s = read_input_file(path)
#     D, k = anneal_solve_20(G, s)
#     assert is_valid_solution(D, G, s, k)
#     print("Total Happiness: {}".format(calculate_happiness(D, G)))
#     write_output_file(D, 'out/test.out')

if __name__ == '__main__':
    inputs = glob.glob('./all_inputs/large-*')
    ttl = len(inputs)
    ct = 0

    for input_path in inputs:
        if ct % 50 == 0:
            print("{} out of {}".format(ct, ttl))

        output_path = './all_outputs/' + basename(normpath(input_path))[:-3] + '.out'

        G, s = read_input_file(input_path, 50)
        D, k = greedy_solve_50(G, s)
        G, s = read_input_file(input_path, 50)
        assert is_valid_solution(D, G, s, k)

        write_output_file(D, output_path)
        ct += 1
