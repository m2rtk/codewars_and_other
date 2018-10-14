

def calc(expression):
    tokens = Lexer(expression).process()
    # todo ast
    pass


class Lexer:

    def __init__(self, expression):
        self.expression = expression
        self.state = self._state_none
        self.output = []

    def process(self):
        for char in self.expression:
            self.state(char)

        return self.output

    def _state_none(self, c):
        if is_symbol(c):
            self.output.append(c)
            return

        if is_digit(c):
            self.state = self._state_number
            self.output.append(c)

    def _state_number(self, c):
        if is_digit(c):
            self.output[-1] += c
            return

        self.state = self._state_none
        self.output[-1] = float(self.output[-1]) if '.' in self.output[-1] else int(self.output[-1])

        if is_symbol(c):
            self.output.append(c)


def is_symbol(c):
    return c in "+-/*()"


def is_digit(c):
    return c in "1234567890."


if __name__ == '__main__':
    tests = [
        ["1 + 1", 2],
        ["8/16", 0.5],
        ["3 -(-1)", 4],
        ["2 + -2", 0],
        ["10- 2- -5", 13],
        ["(((10)))", 10],
        ["3 * 5", 15],
        ["-7 * -(6 / 3)", 14]
    ]

    for test in tests:
        print(f"{test[0]} => {Lexer(test[0]).process()}")