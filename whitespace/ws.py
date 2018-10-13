from whitespace import whitespace
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('filename', help='whitespace file to read and execute')
parser.add_argument('-i', '--input', default='')
parser.add_argument('-d', '--debug', action='store_true')


if __name__ == '__main__':
    args = parser.parse_args()
    whitespace(open(args.filename, 'r').read(), debug=args.debug, inp=args.input)
