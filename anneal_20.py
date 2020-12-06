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

def anneal_solve_20(G, s):
    curr = {}
    rooms = {}

    best_happiness = 0

    for i in range(20):
        curr[i] = 0

    if is_valid_solution(curr, G, s, 1):
        return (curr, 1)

    edgelist = list(G.edges.data())

    edgelist.sort(key = lambda x: -x[2]['happiness'])
    edgelist.sort(key = lambda x: x[2]['stress'])

    for i in range(20):
        curr[i] = i
        rooms[i] = [i]

    best = (dict(curr), 20)

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

    # print(best)

    T = 100000

    G_copy = G.copy()
    for e in list(G_copy.edges.data()):
        if e[2]['stress'] > s / 2:
            G_copy.remove_edge(*e[:2])

    # print("beginning annealing...")
    # print()
    # start = timeit.default_timer()

    for i in range(ITERATIONS):
        # print(T)
        # if i % 100 == 0:
        #     end = timeit.default_timer()
        #     print("{} out of {}, elapsed time: {}".format(i, ITERATIONS, end - start))
        #     start = timeit.default_timer()

        st1 = random.choice(range(20))
        poss_swaps = G_copy.edges(st1)
        st2 = random.choice(list(poss_swaps))[1]

        st1_num, st2_num = curr[st1], curr[st2]
        st1_room, st2_room = rooms[st1_num], rooms[st2_num]

        swap_1 = st1_room[:]
        swap_2 = st2_room + [st1]
        swap_1.remove(st1)

        curr[st1] = st2_num
        num_rooms = max(curr.values()) + 1

        curr_happ = calculate_happiness_for_room(st1_room, G) + calculate_happiness_for_room(st2_room, G)
        swap_happ = calculate_happiness_for_room(swap_1, G) + calculate_happiness_for_room(swap_2, G)

        delta = swap_happ - curr_happ
        # print(delta, st1, st2)
        if delta > 0 and is_valid_solution(curr, G, s, num_rooms):
            # print("in here")
            rooms[st2_num] += [st1]
            st1_room.remove(st1)

        elif random.random() < math.exp(delta / T):
            # print("anneal :0")
            rooms[st2_num] += [st1]
            st1_room.remove(st1)

        else:
            curr[st1] = st1_num

        T *= .99

        rooms = reorder_rooms(rooms)
        curr = convert_dictionary(rooms)
        num_rooms = max(curr.values()) + 1
        if is_valid_solution(curr, G, s, num_rooms):
            happ = calculate_happiness(curr, G)
            if happ > best_happiness:
                best_happiness = happ
                best = (dict(curr), num_rooms)
    # print(best)
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
    inputs = glob.glob('./all_inputs/medium-*')
    ttl = len(inputs)
    ct = 0

    for input_path in inputs:
        if ct % 50 == 0:
            print("{} out of {}".format(ct, ttl))
        print(input_path)
        output_path = './all_outputs/' + basename(normpath(input_path))[:-3] + '.out'

        G, s = read_input_file(input_path, 20)

        D_o = read_output_file(output_path, G, s)
        h_o = calculate_happiness(D_o, G)

        D, k = anneal_solve_20(G, s)
        G, s = read_input_file(input_path, 20)
        assert is_valid_solution(D, G, s, k)

        h = calculate_happiness(D, G)

        if h > h_o:
            print("improvement on {} ({} vs {}), overwriting...".format(input_path, D_o, D))
            write_output_file(D, output_path)
        ct += 1
