import sys
import os
import getopt

from utils import *
from parse import *

def main(argv):
    path = ""

    try:
        opts, args = getopt.getopt(argv,"p:")
    except getopt.GetoptError:
        print('invalid arguments')
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-p":
            path = arg

    solve(path)

def greedy_sort_by_stress(G, num_rooms, stress_per_group):
    edgelist = []
    for e in G.edges.data():
        if e[2]["stress"] < stress_per_group:
            edgelist += [e]
    edgelist.sort(key = lambda x: x[2]["stress"])

    return edgelist

def solve(G, stress_budget):
    num_nodes = len(G)
    num_rooms = 2

    best_matching = ({}, 0)
    best_score = 0

    while num_rooms <= (num_nodes / 2):
        groups = {}
        assts = {}
        stress_per_group = float(stress_budget) / num_rooms
        edgelist = greedy_sort_by_stress(G, num_rooms, stress_per_group)

        for i in range(num_rooms):
            groups[i] = []

        new_room = 0
        print(edgelist)
        for e in edgelist:
            print()
            print(groups)
            print(assts)
            print(e)
            if len(assts) == num_nodes:
                break

            st1, st2, val = e
            p_happiness = val["happiness"]
            p_stress = val["stress"]


            if st1 in assts and st2 in assts:
                st1_room = assts[st1]
                st2_room = assts[st2]

                if st1_room == st2_room:
                    break

                tentative1_1 = groups[st1_room][:] + [st2]
                tentative2_1 = groups[st2_room][:]
                tentative2_1.remove(st2)

                swap_into_1 = calculate_stress_for_room(tentative1_1, G) < stress_per_group

                tentative1_2 = groups[st2_room][:]
                tentative2_2 = groups[st2_room][:] + [st1]
                tentative1_2.remove(st1)

                swap_into_2 = calculate_stress_for_room(tentative2_2, G) < stress_per_group

                st1_curr_hap = calculate_happiness_for_room(groups[st1], G)
                st2_curr_hap = calculate_happiness_for_room(groups[st2], G)

                st1_1_new_hap = calculate_happiness_for_room(tentative1_1, G)
                st2_1_new_hap = calculate_happiness_for_room(tentative2_1, G)

                st1_2_new_hap = calculate_happiness_for_room(tentative1_2, G)
                st2_2_new_hap = calculate_happiness_for_room(tentative2_2, G)

                curr_happ = st1_curr_hap + st2_curr_hap
                swap_to_1_happ = st1_1_new_hap + st2_1_new_hap
                swap_to_2_happ = st1_2_new_hap + st2_2_new_hap

                if swap_to_1_happ > max(swap_to_2_happ, curr_happ) and swap_into_1:
                    assts[st2] = assts[st1]
                    groups[st1_room] += [st2]
                    groups[st2_room].remove(st2)
                    print("moved {} to {}".format(st2, st1))

                elif swap_to_2_happ > max(swap_to_1_happ, curr_happ) and swap_into_2:
                    assts[st1] = assts[st2]
                    groups[st2_room] += [st1]
                    groups[st1_room].remove(st1)
                    print("moved {} to {}".format(st1, st2))

            elif st1 in assts:
                st1_room = assts[st1]
                tentative = groups[st1_room] + [st2]
                if calculate_stress_for_room(tentative, G) < stress_per_group:
                    groups[st1_room] += [st2]
                    assts[st2] = assts[st1]

            elif st2 in assts:
                st2_room = assts[st2]
                tentative = groups[st2_room] + [st1]
                if calculate_stress_for_room(tentative, G) < stress_per_group:
                    groups[st2_room] += [st1]
                    assts[st1] = assts[st2]

            else:
                if new_room >= num_rooms:
                    for i in range(num_rooms):
                        tentative = groups[i] + [st1, st2]
                        if calculate_stress_for_room(tentative, G) < stress_per_group:
                            groups[i] += [st1, st2]
                            assts[st1] = i
                            assts[st2] = i
                            break
                else:
                    groups[new_room] += [st1, st2]
                    assts[st1] = new_room
                    assts[st2] = new_room
                    new_room += 1

        mapping = convert_dictionary(groups)
        score = calculate_happiness(mapping, G)

        if score > best_score:
            best_score = score
            best_matching = (mapping, num_rooms)

        num_rooms += 1

    return best_matching

if __name__ == '__main__':
    assert len(sys.argv) == 2
    path = sys.argv[1]
    G, s = read_input_file(path)
    D, k = solve(G, s)
    assert is_valid_solution(D, G, s, k)
    print("Total Happiness: {}".format(calculate_happiness(D, G)))
    write_output_file(D, './test.out')
