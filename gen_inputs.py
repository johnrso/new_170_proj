import numpy as np

import sys
import os
import getopt
from itertools import combinations
import random

import parse

help = "    HELP: \n\
        n: number of students \n\
        g: number of groups (including stragglers) \n\
        x: number of stragglers, default 0 \n\
        s: maximium stress, default random 0-100 \n\
        d: debug mode, default false\n\
        h: help (display this message)\n\
       "

def main(argv):
    FP = "./inputs/"
    groups = {}
    budgets = {}
    s = np.random.random() * 100
    n = 0
    debug = False
    num_group = 0
    num_strag = 0

    try:
        opts, args = getopt.getopt(argv,"n:g:x:s:dh")
    except getopt.GetoptError:
        print('invalid arguments')
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-n":
            n = int(arg)
        if opt == "-g":
            num_group = int(arg)
        if opt == "-x":
            num_strag = int(arg)
        if opt == "-s":
            s = float(arg)
        if opt == "-d":
            debug = True
        if opt == "-h":
            print(help)
            return 0

    print()
    print("NUMBER OF STUDENTS: {:d}".format(n))
    print("MAX STRESS: {:.3f}".format(s))
    print("NUMBER OF GROUPS (INCLUDING STRAGGLERS): {:d}".format(num_group))
    print("NUMBER OF STRAGGLERS: {:d}".format(num_strag))
    print()

    total_groups = num_group

    students = list(range(n))
    random.shuffle(students)

    for _ in range(num_strag):
        num_group -= 1
        curr = students.pop()
        print("straggler: {:d}".format(curr))

    print()

    while num_group > 0:
        g = []

        if num_group == 1:
            size = len(students)
        else:
            cap = len(students) - 2 * num_group
            if debug: print("cap: {:.2f}".format(cap))
            size = 2 + int(np.random.random() * cap)
        for _ in range(size):
            g += [students.pop()]
        g = tuple(g)

        print("group: " + str(g))

        for i in g:
            groups[i] = g
        budgets[g] = 0

        num_group -= 1

    print()
    print("students remaining: " + str(students))

    s_max = (s / total_groups) - .015 # compensate for rounding error

    for g in budgets:
        budgets[g] = [s_max, len(list(combinations(g, 2))), 0]

    if debug:
        print("total stress: {:.3f}".format(s))
        print("max stress per room: {:.3f}".format(s_max))
        # print(groups)
        # print(budgets)

    out = "{:d} \n".format(n)
    out += "{:.3f} \n".format(s)

    for i in range(n):
        for j in range(i + 1, n):
            s_ij = 0

            if i in groups and j in groups[i]:
                if debug: out += " * " # uncomment to visualize the matched pairs
                curr, num, _ = budgets[groups[i]]
                curr = float(curr)
                if num == 1:
                    s_ij = curr
                else:
                    s_ij = np.random.random() * curr

                budgets[groups[i]][0] -= s_ij
                budgets[groups[i]][1] -= 1
                budgets[groups[i]][2] += s_ij

            else:
                s_ij = np.random.random() * 100

            h_ij = np.random.random() * 100
            out += "{:d} {:d} {:.3f} {:.3f}\n".format(i, j, h_ij, s_ij)

    # if debug:
    #     print(groups)
    #     print(budgets)

    print()
    print("saving...")
    if not os.path.exists(FP):
        try:
            os.mkdir(FP)
        except OSError:
            print("error encountered while creating " + FP)

    FP += "{:d}.in".format(n)
    file = open(FP, 'w+')

    file.write(out)
    file.close()

    print("success! output located at: " + FP)
    print()

    print("testing for well formed input...")

    parse.validate_file(FP)
    try:
        parse.read_input_file(FP)
    except:
        print("input malformed. aborting.")
        print()
        return

    print("success!")
    print()
if __name__ == "__main__":
    main(sys.argv[1:])
