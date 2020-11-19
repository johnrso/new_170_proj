import numpy as np
import sys
import getopt

def main(argv):
    size = 0

    try:
        opts, args = getopt.getopt(argv,"n:",)
    except getopt.GetoptError:
        print('invalid arguments')
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-n":
            size = arg

    

if __name__ == "__main__":
    main(sys.argv[1:])
