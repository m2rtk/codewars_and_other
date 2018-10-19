from random import choice
from operator import add, sub, mul, floordiv, mod


class BefungeInterpreter:

    def __init__(self, code, debug=False):
        self.code = [[c for c in line] for line in code.splitlines()]
        self.debug = debug
        self.x, self.y = 0, 0
        self.dir = self.right
        self.string_mode = False
        self.stack = []
        self.mapping = {
            '+': self.add,
            '-': self.sub,
            '*': self.mul,
            '/': self.div,
            '%': self.mod,
            '!': self.logical_not,
            '`': self.greater_than,
            '>': self.right,
            '<': self.left,
            '^': self.up,
            'v': self.down,
            '?': self.rand_dir,
            '_': self.horizontal_if,
            '|': self.vertical_if,
            '"': self.string,
            ':': self.duplicate,
            '\\': self.swap,
            '$': self.discard,
            '.': self.write_int,
            ',': self.write_char,
            '#': self.bridge,
            'g': self.get,
            'p': self.put,
            '&': self.read_int,
            '~': self.read_char,
            '@': self.end
        }

    def _pop(self):
        if len(self.stack) > 0:
            return self.stack.pop()
        return 0

    def get_current(self):
        c = self.code[self.y][self.x]
        if self.string_mode:
            if c == '"':
                return self.string
            return self.push(ord(c))
        if c in self.mapping:
            return self.mapping[c]
        if c.isdigit() or c.replace('-', '', 1).isdigit():
            return self.push(int(c))

        def no_op():
            pass

        return no_op

    def execute(self):
        while self.x >= 0 and self.y >= 0:
            f = self.get_current()
            if self.debug:
                print()
                print(self.stack)
                print(f.__name__)
            f()
            self.dir()()

    def up(self):
        self.dir = self.up

        def move():
            self.y -= 1

        return move

    def down(self):
        self.dir = self.down

        def move():
            self.y += 1

        return move

    def left(self):
        self.dir = self.left

        def move():
            self.x -= 1

        return move

    def right(self):
        self.dir = self.right

        def move():
            self.x += 1

        return move

    def rand_dir(self):
        self.dir = choice([self.left, self.right, self.up, self.down])

    def string(self):
        self.string_mode = not self.string_mode

    def push(self, x):
        def p():
            self.stack.append(x)
        p.__name__ = 'push_' + str(x)
        return p

    def _math(self, f):
        a = self._pop()
        b = self._pop()
        self.stack.append(f(b, a))

    def add(self):
        self._math(add)

    def sub(self):
        self._math(sub)

    def mul(self):
        self._math(mul)

    def div(self):
        self._math(floordiv)

    def mod(self):
        self._math(mod)

    def logical_not(self):
        self.stack.append(1 if self._pop() == 0 else 0)

    def greater_than(self):
        a = self._pop()
        b = self._pop()
        self.stack.append(1 if b > a else 0)

    def duplicate(self):
        if len(self.stack) > 0:
            self.stack.append(self.stack[-1])

    def swap(self):
        a = self._pop()
        b = self._pop()
        self.stack.append(a)
        self.stack.append(b)

    def discard(self):
        self._pop()

    def write_int(self):
        print(self._pop(), end='')

    def write_char(self):
        print(chr(self._pop()), end='')

    def get(self):
        y = self._pop()
        x = self._pop()

        if y in range(len(self.code)) and x in range(len(self.code[y])):
            self.stack.append(ord(self.code[y][x]))
        else:
            self.stack.append(0)

    def put(self):
        y = self._pop()
        x = self._pop()
        v = self._pop()
        self.code[y][x] = chr(v)

    def read_int(self):
        pass

    def read_char(self):
        pass

    def bridge(self):
        self.dir()()

    def horizontal_if(self):
        if self._pop() == 0:
            self.dir = self.right
        else:
            self.dir = self.left

    def vertical_if(self):
        if self._pop() == 0:
            self.dir = self.down
        else:
            self.dir = self.up

    def end(self):
        self.x, self.y = -1, -1


if __name__ == '__main__':
    BefungeInterpreter((open('sieve.befunge', 'r').read())).execute()
