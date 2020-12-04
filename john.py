import parse
import sys
import os
import getopt

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
    edgeset = {}
    for e in G.edges.data():
        if e[2]["stress"] < stress_per_group:
            edgelist += [e]
            edgeset[e] = 1
    edgelist.sort(key = lambda x: x[2]["stress"])

    return edgelist, edgeset

def add_single(st, groups, num_groups):
    for i in num_groups:
        if i not in groups:
            groups[i]['students'] += [st]
            return True
    return False

def add_pair(st1, st2, groups, g_num):
    if st1 in groups[g_num]['students']:
        if st2 not in groups[g_num]['students']:
            pass
    if st2 in groups[g_num]['students']:
        if st1 not in groups[g_num]['students']:
            pass

    return False

def update_room_budget(new_st, group, edgelist, edgeset):
    budget = group['budget']

    for st in group['students']:
        if st < new_st:
            pair = (st, new_st)
        else:
            pair = (new_st, st)

        if pair in edgeset:
            budget -= edgeset[pair]['stress']
        else:
            return False



def solve(path):
    G, stress_budget = parse.read_input_file(path)
    num_nodes = len(G)
    num_rooms = 1

    best_matching = {}

    while num_rooms <= (num_nodes / 2):
        groups = {}
        assts = {}
        stress_per_group = float(stress_budget) / num_rooms
        edgelist, edgeset = greedy_sort_by_stress(G, num_rooms, stress_per_group)

        for i in range(num_rooms):
            groups[i] = {}
            groups[i]['students'] = []
            groups[i]['budget'] = stress_per_group

        for e in curr_edges:
            st1, st2, val = e
            p_happiness = val["happiness"]
            p_stress = val["stress"]

            if st2 not in groups[assts[st1]]: # if st2 is
                    pass
            elif st2 in assts:
                if st1 not in groups[assts[st2]]:
                    pass
            else:
                for ind in range(num_rooms):
                    if ind not in groups:
                        add_pair(st1, st2, groups, ind)

        num_rooms += 1

if __name__ == "__main__":
    main(sys.argv[1:])
