import numpy as np

import sys
import os
import getopt

def main(argv):
    FP = "./inputs/"
    n = 0
    s = np.random.random() * 100

    try:
        opts, args = getopt.getopt(argv,"n:s",)
    except getopt.GetoptError:
        print('invalid arguments')
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-n":
            n = int(arg)
        if opt == "-s":
            s = float(arg)

    out = "{:d} \n".format(n)
    out += "{:.3f} \n".format(s)

    for i in range(n):
        for j in range(i + 1, n):
            h_ij, s_ij = np.random.random() * 100, np.random.random() * 100
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
