from brainfuck import BrainfuckInterpreter
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('filename', help='brainfuck file to read and execute, leave empty to read from stdin', nargs='?')
parser.add_argument('-d', '--debug', action='store_true')


if __name__ == '__main__':
    args = parser.parse_args()

    if args.filename:
        code = open(args.filename, 'r').read()
    else:
        code = sys.stdin.read()

    BrainfuckInterpreter(code, debug=args.debug).execute()
