import string


def assembler_interpreter(program):
    engine = Engine(debug=True)
    engine.execute(Lexer(program).process())
    return engine.output


class Lexer:
    def __init__(self, code):
        self.code = code
        self.state = self._state_none
        self.acc = ""

    def process(self):
        return [self.parse(line) for line in self.code.splitlines() if line.strip() and not line.strip().startswith(";")]

    def parse(self, line):
        line = line.strip()
        cmd, *args = line.split(None, 1)

        if args:
            args = self.parse_args(args[0])
        else:
            if cmd.endswith(":"):
                args = [cmd[:-1]]
                cmd = "label"
            elif cmd not in ('ret', 'end'):
                raise RuntimeError

        return cmd, tuple(args)

    def parse_args(self, args):
        self.state = self._state_none

        def generator():
            for c in args:
                if self.state:
                    yield self.state(c)
            if self.acc:
                yield self.acc

        return [token for token in generator() if token or type(token) is int]

    def _state_none(self, c):
        self.acc = ""

        if c == ";":
            self.state = None
            return

        if c == "'":
            self.state = self._state_string
            self.acc = c
            return

        if c in string.ascii_letters:
            self.state = self._state_label
            self.acc = c
            return

        if c in string.digits:
            self.state = self._state_num
            self.acc = c
            return

    def _state_label(self, c):
        if c == ",":
            pass
        elif c in string.ascii_letters or c in string.digits or c in string.punctuation:
            self.acc += c
            return

        self.state = self._state_none
        return self.acc

    def _state_string(self, c):
        self.acc += c
        if c == "'":
            self.state = self._state_none
            return self.acc

    def _state_num(self, c):
        if c in string.digits:
            self.acc += c
            return

        self.state = self._state_none
        return int(self.acc)


def is_digit(s):
    if s[0] in ('-', '+'):
        return s[1:].isdigit()
    return s.isdigit()


class Engine:

    def __init__(self, debug=False):
        self.registers = {}
        self.instructions = []
        self.labels = {}
        self.subroutine_call_pos = []
        self.pos = -1
        self.debug = debug
        self.last_cmp = None

        self.tmp_output = ""
        self.output = -1

    def execute(self, instructions):
        self.instructions = instructions
        self._pre_process()

        if self.debug:
            print(self.instructions)
            print(self.labels)

        self.pos = 0
        while -1 < self.pos < len(self.instructions):
            f, n = self.instructions[self.pos]

            if f == 'label':
                self.pos += 1
                continue

            f = getattr(self, f)
            if self.debug:
                print(self.pos)
                print(self.registers)
                print(f.__name__, *n)
                print()
            f(*n)
            self.pos += 1

    def _get(self, x):
        if type(x) == int or is_digit(x):
            return int(x)
        return self.registers[x]

    def _pre_process(self):
        for i, ii in enumerate(self.instructions):
            if ii[0] == 'label':
                self.labels[ii[1][0]] = i

    def mov(self, x, y):
        self.registers[x] = self._get(y)

    def inc(self, x):
        self.registers[x] += 1

    def dec(self, x):
        self.registers[x] -= 1

    def jnz(self, x, y):
        if self._get(x) != 0:
            self.pos += int(y) - 1

    def add(self, x, y):
        self.registers[x] += self._get(y)

    def sub(self, x, y):
        self.registers[x] -= self._get(y)

    def mul(self, x, y):
        self.registers[x] *= self._get(y)

    def div(self, x, y):
        self.registers[x] //= self._get(y)

    def label(self, name, pos):
        self.labels[name] = pos

    def jmp(self, name):
        self.pos = self.labels[name] - 1  # -1 could be bad

    def cmp(self, x, y):
        x, y = self._get(x), self._get(y)
        if x == y:
            self.last_cmp = 0
        elif x >= y:
            self.last_cmp = 1
        elif x < y:
            self.last_cmp = -1

    def jne(self, label):
        if self.last_cmp != 0:
            self.jmp(label)

    def je(self, label):
        if self.last_cmp == 0:
            self.jmp(label)

    def jge(self, label):
        if self.last_cmp in (0, 1):
            self.jmp(label)

    def jg(self, label):
        if self.last_cmp == 1:
            self.jmp(label)

    def jle(self, label):
        if self.last_cmp in (0, -1):
            self.jmp(label)

    def jl(self, label):
        if self.last_cmp == -1:
            self.jmp(label)

    def call(self, label):
        self.subroutine_call_pos.append(self.pos)
        self.jmp(label)

    def ret(self):
        self.pos = self.subroutine_call_pos.pop()

    def msg(self, *args):
        self.tmp_output = ""
        for arg in args:
            if arg[0] == "'" and arg[-1] == "'":
                arg = arg[1:][:-1]
            else:
                arg = self._get(arg)

            self.tmp_output += str(arg)

    def end(self):
        self.output = self.tmp_output
        self.pos = -2
