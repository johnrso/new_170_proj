import os
import numpy as np

def create_input(filename, sets, S_max):
    file1 = open(filename, 'r') 
    lines = file1.readlines()
    n = int(lines[0])

    store = [[[0,0] for _ in range(n)] for _ in range(n)]

    # store values
    for k in lines[2:]:
        vals = k.split()
        store[int(vals[0])][int(vals[1])] = [float(vals[2]), float(vals[3])]
    
    # Randomize stress for values that arent edges
    for i in range(n):
        for j in range(i, n):
            if i != j:
                if not sameset(i, j, sets):
                    store[i][j][1] = 30 + np.random.random() * 70; 

    _, stress = output(sets, store)
    S = sum(stress)

    for k in sets:
        a = list(k)
        for i in range(len(a)):
            for j in range(i, len(a)):
                if i != j:
                    store[min(a[i], a[j])][max(a[i], a[j])][1] /= S 
                    store[min(a[i], a[j])][max(a[i], a[j])][1] *= S_max

    return store, n

def sameset(i, j, sets):
    for k in sets:
        if i in k:
            if j in k:
                return True
            return False
    return False

def output(sets, vals):
    happiness = []
    stress = []
    for k in sets:
        hap = 0
        sts = 0
        a = list(k)
        for i in range(len(a)):
            for j in range(i, len(a)):
                if i != j:
                    hap += vals[min(a[i], a[j])][max(a[i], a[j])][0]
                    sts += vals[min(a[i], a[j])][max(a[i], a[j])][1]

        happiness.append(hap)
        stress.append(sts)
    return happiness, stress

def print_input(n, vals, s_max):
    print(n)
    print(s_max)
    for i in range(n):
        for j in range(i, n):
            if i != j:
                print(i, j, vals[i][j][0], vals[i][j][1])

# ACTUAL CODE RUNNING
sets = [set([0, 8, 6]), set([1, 3, 5]), set([2, 7, 9])]
s_max = 90
s, n = create_input('inputs/10.in', sets, s_max)
print_input(n, s, s_max)
print(output(sets, s))

