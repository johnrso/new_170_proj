import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import parse
import sys
import random
from collections import defaultdict
from utils import is_valid_solution, calculate_happiness, calculate_stress_for_room

if __name__ == "__main__":
    assert len(sys.argv) >= 2
    path = sys.argv[1]
    G, stress_budget = parse.read_input_file(path)

    groups = 4

    stress_per_group = stress_budget/float(groups) #num groups

    edges = []
    for e in G.edges.data():
        print(e, e[2]["stress"] < stress_per_group)
        if e[2]["stress"] < stress_per_group:
            edges.append(e)
    g = defaultdict(lambda: [])
    edges.sort(key = lambda x: x[2]["stress"], reverse=True)

    placed = defaultdict(lambda: -1)

    n = G.number_of_nodes()
    for i in range(n):
        s = edges[i][0]
        e = edges[i][1]
        if placed[s] == -1 and placed[e] == -1:
            vals = list(range(0, groups))
            x = random.choice(vals)
            while calculate_stress_for_room(g[x] + [s], G) > stress_per_group:
                vals.remove(x)
                x = random.choice(vals)
                if vals == []:
                    print("doesn't work")
                    exit()

            vals = list(range(0, groups))
            vals.remove(x)
            y = random.choice(vals)

            while calculate_stress_for_room(g[y] + [e], G) > stress_per_group:
                vals.remove(y)
                y = random.choice(vals)
                if vals == []:
                    print("doesn't work")
                    exit()

            placed[s] = x
            placed[e] = y
            g[x].append(s)
            g[y].append(e)
            
        elif placed[s] == -1:
            x = placed[e]
            vals = list(range(0, groups))
            vals.remove(x)
            y = random.choice(vals)
            
            while calculate_stress_for_room(g[y] + [s], G) > stress_per_group:
                vals.remove(y)
                y = random.choice(vals)
                if vals == []:
                    print("doesn't work")
                    exit()

            placed[s] = y
            g[y].append(s)

        elif placed[e] == -1:
            x = placed[s]

            vals = list(range(0, groups))
            vals.remove(x)
            y = random.choice(vals)

            while calculate_stress_for_room(g[y] + [e], G) > stress_per_group:
                vals.remove(y)
                y = random.choice(vals)
                if vals == []:
                    print("doesn't work")
                    exit()

            placed[s] = y
            g[y].append(e)
    print(g)
    print(calculate_happiness(placed, G))
    assert is_valid_solution(placed, G, stress_budget, groups)
