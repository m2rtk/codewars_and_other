import string


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
