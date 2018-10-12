from whitespace import whitespace
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('filename', help='whitespace file to read and execute')
parser.add_argument('-i', '--input', default='')
parser.add_argument('-d', '--debug', action='store_true')


if __name__ == '__main__':
    args = parser.parse_args()
    filename = args.filename
    debug = args.debug
    input = args.input
    print(whitespace(open(filename, 'r').read(), debug=debug, inp=input))
