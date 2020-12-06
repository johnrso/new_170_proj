import sys
import os
import getopt
import glob
import math

from utils import *
from parse import *
from os.path import *

if __name__ == '__main__':
    inputs = glob.glob('./all_inputs/medium-*')
    ttl = len(inputs)
    print(ttl)
    ct = 0
    for input_path in inputs:
        if ct % 50 == 0:
            print("{} out of {}".format(ct, ttl))
        output_path = './all_outputs/' + basename(normpath(input_path))[:-3] + '.out'
        print(input_path, output_path)

        G, s = read_input_file(input_path, 20)
        D = read_output_file(output_path, G, s)

        ct += 1
