import sys


class BrainfuckInterpreter:
    def __init__(self, code, debug=False):
        self.command_mapping = self._generate_command_mapping()
        self.tokens = [t for t in code if t in self.command_mapping]
        self.tape = [0]
        self.pointer = 0
        self.pos = 0
        self.debug = debug
        self.debug_output = ""

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
        self.tape[self.pointer] = ord(sys.stdin.read(1))

    def jump_if_zero(self):
        if self.tape[self.pointer] == 0:
            new_pos = self.pos
            while self.tokens[new_pos] != ']':
                new_pos += 1

            self.pos = new_pos + 1

    def jump_if_not_zero(self):
        if self.tape[self.pointer] != 0:
            new_pos = self.pos
            open_brackets = 0

            while new_pos > -1:
                new_pos -= 1
                t = self.tokens[new_pos]

                if t == ']':
                    open_brackets += 1
                elif t == '[':
                    open_brackets -= 1
                else:
                    continue

                if open_brackets == 0:
                    break

            self.pos = new_pos
