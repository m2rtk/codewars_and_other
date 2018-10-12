from copy import deepcopy

nums = set(range(1, 10))
indices = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]


def sudoku_solver(puzzle):
    return rec(State(puzzle))


def rec(state):
    next_move = state.next_empty_cell()
    if next_move is None:
        return state.sudoku

    for possibility in state.get_possible(*next_move):
        next_state = state.set(*next_move, possibility)
        if next_state.valid():
            res = rec(next_state)
            if res is not None:
                return res


def valid(unit):
    unit = [i for i in unit if i != 0]
    s = set(unit)
    return len(s) == len(unit) and all(ss in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] for ss in s)


class State(object):
    def __init__(self, sudoku, last_move=None):
        self.sudoku = sudoku
        self.last_move = last_move

    def get(self, y, x):
        return self.sudoku[y][x]

    def set(self, y, x, n):
        copy = self.sudoku
        copy[y][x] = n
        return State(copy, (y, x))

    def get_possible(self, y, x):
        n = self.get(y, x)

        if n != 0:
            return []

        return nums.difference(set(self.row(y) + self.col(x) + self.box(y, x)))

    def next_empty_cell(self):
        if self.last_move is None:
            return 0, 0
        y, x = self.last_move

        while True:
            x += 1
            if x == 9:
                y += 1
                x = 0

            if y == 9:
                return None

            if self.get(y, x) == 0:
                return y, x

    def row(self, y):
        return self.sudoku[y]

    def valid_row(self, y):
        return valid(self.row(y))

    def col(self, x):
        return list([*zip(*self.sudoku)][x])

    def valid_col(self, x):
        return valid(self.col(x))

    def box(self, y, x):
        return [self.sudoku[(y // 3) * 3 + yy][(x // 3) * 3 + xx] for yy, xx in indices]

    def valid_box(self, y, x):
        return valid(self.box(y, x))

    def valid_cell(self, y, x):
        return self.valid_row(y) and self.valid_col(x) and self.valid_box(y, x)

    def valid(self):
        return self.valid_cell(*self.last_move)