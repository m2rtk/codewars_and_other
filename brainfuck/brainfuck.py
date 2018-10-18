import sys


class BrainfuckInterpreter:
    def __init__(self, code, debug=False):
        self.command_mapping = self._generate_command_mapping()
        self.tokens = [t for t in code if t in self.command_mapping]
        self.bracket_pairs = self._generate_bracket_pairs()
        self.debug = debug
        self.debug_output = ""

        self.tape = [0]
        self.pointer = 0
        self.pos = 0

    def _generate_command_mapping(self):
        return {
            '>': self.mov_right,
            '<': self.mov_left,
            '+': self.increment,
            '-': self.decrement,
            '.': self.output,
            ',': self.input,
            '[': self.jump_if_zero,
            ']': self.jump_if_not_zero,
        }

    def _generate_bracket_pairs(self):
        pairs = {}
        open_stack = []
        for i, t in filter(lambda x: x[1] in '[]', enumerate(self.tokens)):
            if t == '[':
                open_stack.append(i)
            elif t == ']':
                if not open_stack:
                    raise RuntimeError("Unmatched ']'")

                start = open_stack.pop()
                end = i
                pairs[start] = end
                pairs[end] = start

        if open_stack:
            raise RuntimeError("Unmatched '['")

        return pairs

    def debug_print(self):
        if self.debug:
            print(f"{''.join(self.tokens)}")
            print(f"{' ' * self.pos}^ {self.pos}")
            print(f"tape: {self.tape}.at(pointer={self.pointer}) => {self.tape[self.pointer]}")
            print(f"current output: '{self.debug_output}'")
            print()

    def execute(self):
        self.debug_print()
        while self.pos < len(self.tokens):
            f = self.command_mapping[self.tokens[self.pos]]
            self.pos += 1
            f()
            self.debug_print()

    def mov_right(self):
        self.pointer += 1
        if self.pointer == len(self.tape):
            self.tape.append(0)

    def mov_left(self):
        self.pointer -= 1
        if self.pointer < 0:
            self.pointer = 0

    def increment(self):
        self.tape[self.pointer] += 1
        self.tape[self.pointer] &= 0xff

    def decrement(self):
        self.tape[self.pointer] -= 1
        self.tape[self.pointer] &= 0xff

    def output(self):
        print(chr(self.tape[self.pointer]), end='')

        if self.debug:
            self.debug_output += chr(self.tape[self.pointer])

    def input(self):
        byte = sys.stdin.read(1)
        if byte:
            self.tape[self.pointer] = ord(byte)

    def jump_if_zero(self):
        if self.tape[self.pointer] == 0:
            self.pos = self.bracket_pairs[self.pos - 1]

    def jump_if_not_zero(self):
        if self.tape[self.pointer] != 0:
            self.pos = self.bracket_pairs[self.pos - 1]
