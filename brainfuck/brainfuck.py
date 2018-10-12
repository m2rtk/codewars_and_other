import sys


class Engine:
    def __init__(self, code, debug=False):
        self.tokens = [c for c in code if c in "><+-.,[]"]
        self.tape = [0]
        self.pointer = 0
        self.pos = 0
        self.debug = debug

    def execute(self):
        while self.pos < len(self.tokens):
            f = {
                '>': self.mov_right,
                '<': self.mov_left,
                '+': self.increment,
                '-': self.decrement,
                '.': self.output,
                ',': self.input,
                '[': self.jump_if_zero,
                ']': self.jump_if_not_zero,
            }[self.tokens[self.pos]]
            if self.debug:
                print(self.pos)
                print(self.tape)
                print(self.pointer)
                print(f.__name__)
                print()
            self.pos += 1
            f()

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
            open = 0

            while new_pos > -1:
                new_pos -= 1
                c = self.tokens[new_pos]
                if c == ']': open += 1
                elif c == '[': open -= 1

                if open == 0:
                    break

            self.pos = new_pos


if __name__ == '__main__':
    c = "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++."
    #c = ">++++++++[-<+++++++++>]<.>>+>-[+]++>++>+++[>[->+++<<+++>]<<]>-----.>->+++..+++.>-.<<+[>[+>+]>>]<--------------.>>.+++.------.--------.>+.>+."
    c = "--<-<<+[+[<+>--->->->-<<<]>]<<--.<++++++.<<-..<<.<+.>>.>>.<<<.+++.>>.>>-.<<<+."
    #c = "+[-->-[>>+>-----<<]<--<---]>-.>>>+.>>..+++[.>]<<<<.+++.------.<<-.>>>>+."
    e = Engine(c, False)
    e.execute()