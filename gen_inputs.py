import numpy as np

import sys
import os
import getopt
from itertools import combinations

def main(argv):
    FP = "./inputs/"
    groups = {}
    budgets = {}
    s = np.random.random() * 100
    debug = False

    try:
        opts, args = getopt.getopt(argv,"n:g:s:d")
    except getopt.GetoptError:
        print('invalid arguments')
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-n":
            n = int(arg)
        if opt == "-g":
            spl = arg.split()
            for g in spl:
                budgets[g] = 0
                for i in g:
                    groups[i] = g;
        if opt == "-s":
            s = float(arg)
        if opt == "-d":
            debug = True


    strag = n - len(groups)
    s_max = (s / (len(budgets) + strag)) - .015 # compensate for rounding error

    for g in budgets:
        budgets[g] = [s_max, len(list(combinations(g, 2))), 0]

    if debug:
        print(s)
        print(s_max)
        print(strag)
        print(groups)
        print(budgets)

    out = "{:d} \n".format(n)
    out += "{:.3f} \n".format(s)

    for i in range(n):
        for j in range(i + 1, n):
            s_ij = 0

            if str(i) in groups and str(j) in groups[str(i)]:
                if debug: out += " * " # uncomment to visualize the matched pairs
                curr, num, _ = budgets[groups[str(i)]]
                curr = float(curr)
                if num == 1:
                    s_ij = curr
                else:
                    s_ij = np.random.random() * curr

                budgets[groups[str(i)]][0] -= s_ij
                budgets[groups[str(i)]][1] -= 1
                budgets[groups[str(i)]][2] += s_ij

            else:
                s_ij = np.random.random() * 100

            h_ij = np.random.random() * 100
            out += "{:d} {:d} {:.3f} {:.3f} \n".format(i, j, h_ij, s_ij)

    if not os.path.exists(FP):
        try:
            os.mkdir(FP)
        except OSError:
            print("error encountered while creating " + FP)

    FP += "{:d}.in".format(n)
    file = open(FP, 'w+')

    file.write(out)
    file.close()

if __name__ == "__main__":
    main(sys.argv[1:])
