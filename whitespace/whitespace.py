from enum import Enum
from operator import add, sub, mul, floordiv, mod


class Symbol(Enum):
    space = " "
    tab = "\t"
    line_feed = "\n"

    @classmethod
    def exists(cls, value):
        return any(value == item.value for item in cls)

    def __repr__(self):
        return f"{self.name.upper()}"


SPACE = Symbol.space
TAB = Symbol.tab
LINE_FEED = Symbol.line_feed
NUMBER = 0
LABEL = 1


def whitespace(code, inp='', debug=False):
    engine = WhitespaceInterpreter(
        code,
        inp=inp,
        stack=[],
        heap={},
        debug=debug
    )

    return engine.execute()


# noinspection PyDefaultArgument
class WhitespaceInterpreter:
    def __init__(self, code, inp='', stack=[], heap={}, debug=False, output_to_stdout=True):
        self.code = code
        self.tokens = list(map(Symbol, filter(Symbol.exists, code)))
        self.inp = inp
        self.heap = heap
        self.stack = stack
        self.debug = debug
        self.output_to_stdout = output_to_stdout
        self.output = ''
        self.pos = 0
        self.commands = []

        self.parser = Parser(self)

        self.flow_control = FlowControl(self)
        self.io = IO(self)
        self.stack_manipulation = StackManipulation(self)
        self.heap_access = HeapAccess(self)
        self.arithmetic = Arithmetic(self)

        self.full_mapping = self._full_mapping()

    def execute(self):
        self.commands = self.parser.parse_commands()

        if self.debug:
            for i, f in enumerate(self.commands):
                if type(f) == tuple:
                    f, n = f
                    print(f"{i}: {f.__name__}({n if len(str(n)) != 0 else '<empty_string>'})")
                else:
                    print(f"{i}: {f.__name__}()")
            print()

        # add all marks to flow_control labels
        for pos, f in enumerate(self.commands):
            if type(f) == tuple:
                f, n = f
                if f.__name__ == 'mark':
                    self.flow_control.add_label(n, pos, correction=0)

        while -1 < self.pos < len(self.commands):
            if self.debug:
                print(f"heap: {self.heap}")
                print(f"stack: {self.stack}")
                print(f"labels: {self.flow_control.labels}")

            f = self.commands[self.pos]
            self.pos += 1

            if type(f) == tuple:
                f, n = f
                if self.debug: print(f"{self.pos - 1}: {f.__name__}({n if len(str(n)) != 0 else '<empty_string>'})")
                f(n)
            else:
                if self.debug: print(f"{self.pos - 1}: {f.__name__}()")
                f()

            if self.debug: print()

        if self.pos is not -1:
            raise RuntimeError("Unclean termination")

        return self.output

    def _full_mapping(self):
        return {
            (SPACE, SPACE, NUMBER): self.stack_manipulation.push,
            (SPACE, TAB, SPACE, NUMBER): self.stack_manipulation.duplicate_n,
            (SPACE, TAB, LINE_FEED, NUMBER): self.stack_manipulation.discard_n,
            (SPACE, LINE_FEED, SPACE): self.stack_manipulation.duplicate,
            (SPACE, LINE_FEED, TAB): self.stack_manipulation.swap,
            (SPACE, LINE_FEED, LINE_FEED): self.stack_manipulation.discard,

            (TAB, SPACE, SPACE, SPACE): self.arithmetic.add,
            (TAB, SPACE, SPACE, TAB): self.arithmetic.sub,
            (TAB, SPACE, SPACE, LINE_FEED): self.arithmetic.mul,
            (TAB, SPACE, TAB, SPACE): self.arithmetic.div,
            (TAB, SPACE, TAB, TAB): self.arithmetic.mod,

            (TAB, TAB, SPACE): self.heap_access.write,
            (TAB, TAB, TAB): self.heap_access.read,

            (TAB, LINE_FEED, SPACE, SPACE): self.io.print_char,
            (TAB, LINE_FEED, SPACE, TAB): self.io.print_num,
            (TAB, LINE_FEED, TAB, SPACE): self.io.input_char,
            (TAB, LINE_FEED, TAB, TAB): self.io.input_num,

            (LINE_FEED, SPACE, SPACE, LABEL): self.flow_control.mark,
            (LINE_FEED, SPACE, TAB, LABEL): self.flow_control.call,
            (LINE_FEED, SPACE, LINE_FEED, LABEL): self.flow_control.jump,
            (LINE_FEED, TAB, SPACE, LABEL): self.flow_control.jump_if_zero,
            (LINE_FEED, TAB, TAB, LABEL): self.flow_control.jump_if_lt_zero,
            (LINE_FEED, TAB, LINE_FEED): self.flow_control.exit_subroutine,
            (LINE_FEED, LINE_FEED, LINE_FEED): self.flow_control.exit_program
        }


class Controller:
    def __init__(self, engine):
        self.engine = engine


class StackManipulation(Controller):
    def __init__(self, engine):
        super().__init__(engine)

    def push(self, n):
        self.engine.stack.append(n)

    def duplicate_n(self, n):
        assert len(self.engine.stack) > n > -1
        self.engine.stack.append(self.engine.stack[-(n + 1)])

    def discard_n(self, n):
        assert len(self.engine.stack) > 0
        if n < 0 or n >= len(self.engine.stack):
            self.engine.stack = [self.engine.stack[-1]]
        else:
            self.engine.stack = self.engine.stack[:-(n + 1)] + [self.engine.stack[-1]]

    def duplicate(self):
        self.duplicate_n(0)

    def swap(self):
        assert len(self.engine.stack) > 1
        tmp = self.engine.stack[-1]
        self.engine.stack[-1] = self.engine.stack[-2]
        self.engine.stack[-2] = tmp

    def discard(self):
        assert len(self.engine.stack) > 0
        self.engine.stack = self.engine.stack[:-1]


class FlowControl(Controller):
    def __init__(self, engine):
        super().__init__(engine)
        self.labels = {}
        self.subroutine_start = -1

    def add_label(self, label, pos=None, correction=1):
        pos = pos or self.engine.pos
        if label in self.labels and self.labels[label] != pos - correction:
            raise KeyError("Label already exists")
        self.labels[label] = pos

    def get_pos(self, label):
        if label not in self.labels:
            raise KeyError("No such label defined")
        return self.labels[label]

    def mark(self, label):
        self.add_label(label)

    def call(self, label):
        self.subroutine_start = self.engine.pos
        self.jump(label)

    def jump(self, label):
        self.engine.pos = self.get_pos(label)

    def jump_if_zero(self, label):
        if self.engine.stack.pop() == 0:
            self.jump(label)

    def jump_if_lt_zero(self, label):
        if self.engine.stack.pop() < 0:
            self.jump(label)

    def exit_subroutine(self):
        if self.subroutine_start == -1:
            raise RuntimeError("exit outside of subroutine call")
        self.engine.pos = self.subroutine_start

    def exit_program(self):
        self.engine.pos = -1


class IO(Controller):
    def __init__(self, engine):
        super().__init__(engine)
        self.input_pos = 0

    def _read_next_char(self):
        if self.input_pos < len(self.engine.inp):
            c = self.engine.inp[self.input_pos]
            self.input_pos += 1
            return c
        raise EOFError

    def _read_next_int(self):
        i = ""
        while True:
            c = self._read_next_char()

            if c == '\n':
                break

            i += c

        return int(i)

    def print_char(self):
        a = self.engine.stack.pop()
        if type(a) == int:
            a = chr(a)

        self.engine.output += a
        if self.engine.output_to_stdout:
            print(a, end='')

    def print_num(self):
        a = str(self.engine.stack.pop())
        self.engine.output += str(self.engine.stack.pop())
        if self.engine.output_to_stdout:
            print(a, end='')

    def input_char(self):
        self._do_input(self._read_next_char)

    def input_num(self):
        self._do_input(self._read_next_int)

    def _do_input(self, read_f):
        a = read_f()
        b = self.engine.stack.pop()
        self.engine.heap[b] = a


class HeapAccess(Controller):
    def __init__(self, engine):
        super().__init__(engine)

    def write(self):
        a, b = self.engine.stack.pop(), self.engine.stack.pop()
        self.engine.heap[b] = a

    def read(self):
        a = self.engine.stack.pop()
        self.engine.stack.append(self.engine.heap[a])


class Arithmetic(Controller):
    def __init__(self, engine):
        super().__init__(engine)

    def _do(self, f):
        a, b = self.engine.stack.pop(), self.engine.stack.pop()
        self.engine.stack.append(f(b, a))

    def add(self):
        self._do(add)

    def sub(self):
        self._do(sub)

    def mul(self):
        self._do(mul)

    def div(self):
        self._do(floordiv)

    def mod(self):
        self._do(mod)


class Parser:
    def __init__(self, engine):
        self.tokens = engine.tokens
        self.engine = engine
        self.pos = 0

        if len(self.tokens) == 0:
            raise RuntimeError

    def next_token(self):
        token = self.tokens[self.pos]
        self.pos += 1
        return token

    def has_next_token(self):
        return self.pos + 1 < len(self.tokens)

    def parse_number(self):
        sign_token = self.next_token()
        if sign_token is SPACE:
            sign = 1
        elif sign_token is TAB:
            sign = -1
        else:
            raise RuntimeError("Invalid number, no sign specified")

        acc = ""

        bit = self.next_token()

        while bit is not LINE_FEED:
            if bit is SPACE: acc += "0"
            if bit is TAB:   acc += "1"
            bit = self.next_token()

        if len(acc) == 0:
            return 0

        return sign * int(acc, 2)

    def parse_label(self):
        bit = self.next_token()
        label = ""

        while bit is not LINE_FEED:
            if bit is SPACE: label += "0"
            if bit is TAB:   label += "1"
            bit = self.next_token()

        return label

    def parse_next_command(self, current=()):
        current += (self.next_token(),)

        if current in self.engine.full_mapping:
            return self.engine.full_mapping[current]
        elif current + (NUMBER,) in self.engine.full_mapping:
            return self.engine.full_mapping[current + (NUMBER,)], self.parse_number()
        elif current + (LABEL,) in self.engine.full_mapping:
            return self.engine.full_mapping[current + (LABEL,)], self.parse_label()
        else:
            return self.parse_next_command(current)

    def parse_commands(self):
        commands = []

        while self.has_next_token():
            commands.append(self.parse_next_command())
            if self.engine.debug:
                print(commands[-1])

        return commands
